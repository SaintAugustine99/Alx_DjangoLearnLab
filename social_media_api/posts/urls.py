from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)


app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),
]