# accounts/serializers.py

# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 
                  'follower_count', 'following_count', 'created_at')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'created_at': {'read_only': True}
        }
    
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # Using get_user_model().objects.create_user explicitly as required
        user = get_user_model().objects.create_user(**validated_data)
        # Create token for the user
        Token.objects.create(user=user)
        return user
    
    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile."""
    
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 
                  'followers', 'following', 'follower_count', 'following_count', 
                  'created_at', 'updated_at')
        read_only_fields = ('email', 'username', 'created_at', 'updated_at')
    
    def get_followers(self, obj):
        """Get the list of followers."""
        return UserMinimalSerializer(obj.followers.all(), many=True).data
    
    def get_following(self, obj):
        """Get the list of users being followed."""
        return UserMinimalSerializer(obj.following.all(), many=True).data

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for user representation (used in followers/following lists)."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture')

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object."""
    
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Validate and authenticate the user."""
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user'] = user
        return attrs