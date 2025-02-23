# relationship_app/views.py
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Custom registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Class-based login view
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'  # Use the login template
    redirect_authenticated_user = True  # Redirect authenticated users

# Class-based logout view
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'  # Use the logout template

