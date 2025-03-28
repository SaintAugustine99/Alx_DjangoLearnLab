"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""URL configuration for social_media_api project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the home view from the project-level views file
from . import views

# Define URL patterns
urlpatterns = [
    # Root URL - home page
    path('', views.home, name='home'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # API urls
    path('api/accounts/', include('accounts.urls')),
    
    # DRF authentication
    path('api-auth/', include('rest_framework.urls')),

     # ... other URL patterns
    path('api/', include('posts.urls')),

    # ... other URL patterns
    path('api-auth/', include('rest_framework.urls')),
    path('api/posts/', include('posts.urls', namespace='posts')),
    path('api/', include('notifications.urls', namespace='notifications')),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)