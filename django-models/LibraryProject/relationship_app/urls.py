# relationship_app/urls.py
from django.urls import path
from .views import register, path, include, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView
views.register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('admin/', admin.site.urls),
    path('relationship_app/', include('relationship_app.urls')),
]