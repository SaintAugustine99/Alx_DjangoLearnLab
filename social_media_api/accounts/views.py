from django.shortcuts import render

# Create your views here.
# accounts/views.py

from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, 
    AuthTokenSerializer, 
    UserProfileSerializer,
    UserMinimalSerializer,
    UserFollowSerializer,
    FollowerSerializer,
)


User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

class FollowUserView(APIView):
    """Follow/unfollow a user."""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        """Follow a user."""
        try:
            user_to_follow = User.objects.get(id=user_id)
            if user_to_follow == request.user:
                return Response(
                    {'error': 'You cannot follow yourself.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request.user.follow(user_to_follow)
            return Response(
                {'message': f'You are now following {user_to_follow.username}.'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, user_id):
        """Unfollow a user."""
        try:
            user_to_unfollow = User.objects.get(id=user_id)
            request.user.unfollow(user_to_unfollow)
            return Response(
                {'message': f'You have unfollowed {user_to_unfollow.username}.'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserFollowersView(generics.ListAPIView):
    """View to list all followers of a user."""
    serializer_class = UserMinimalSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return the followers for the user."""
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            return user.followers.all()
        except User.DoesNotExist:
            return User.objects.none()

class UserFollowingView(generics.ListAPIView):
    """View to list all users being followed by a user."""
    serializer_class = UserMinimalSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return the users being followed by the user."""
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            return user.following.all()
        except User.DoesNotExist:
            return User.objects.none()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request):
    serializer = UserFollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow = get_object_or_404(User, id=serializer.validated_data['user_id'])
        
        # Don't allow users to follow themselves
        if request.user.id == user_to_follow.id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if already following
        if user_to_follow in request.user.following.all():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request):
    serializer = UserFollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_unfollow = get_object_or_404(User, id=serializer.validated_data['user_id'])
        
        # Check if actually following
        if user_to_unfollow not in request.user.following.all():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request):
    followers = request.user.followers.all()
    serializer = FollowerSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request):
    following = request.user.following.all()
    serializer = FollowerSerializer(following, many=True)
    return Response(serializer.data)