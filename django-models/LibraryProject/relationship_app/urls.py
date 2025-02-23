# relationship_app/urls.py
from django.urls import path
from .views import register, CustomLoginView, CustomLogoutView

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]