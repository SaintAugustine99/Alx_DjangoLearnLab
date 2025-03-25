from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    
    def get_queryset(self):
        """
        Return only the authenticated user's notifications
        """
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
    
    @action(detail=False, methods=['GET'])
    def unread(self, request):
        """
        Return only unread notifications
        """
        unread_notifications = self.get_queryset().filter(read=False)
        
        page = self.paginate_queryset(unread_notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def mark_all_read(self, request):
        """
        Mark all notifications as read
        """
        self.get_queryset().update(read=True)
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def mark_read(self, request, pk=None):
        """
        Mark a specific notification as read
        """
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def mark_unread(self, request, pk=None):
        """
        Mark a specific notification as unread
        """
        notification = self.get_object()
        notification.read = False
        notification.save()
        return Response({"detail": "Notification marked as unread."}, status=status.HTTP_200_OK)