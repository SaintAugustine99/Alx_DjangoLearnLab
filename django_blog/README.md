Documentation: How the Authentication System Works
Overview
The authentication system for the Django blog includes user registration, login, logout, and profile management. It utilizes Django's built-in authentication system with custom extensions for additional functionality.
Components

User Registration:

Uses an extended version of Django's UserCreationForm to include email and name fields.
Handles user registration through a custom view.
Provides feedback on successful registration.


User Login:

Uses Django's built-in LoginView with a custom template.
Redirects to the homepage after successful login.


User Logout:

Uses Django's built-in LogoutView with a custom template.
Provides a confirmation message and options to log back in.


Profile Management:

Custom view for viewing and updating user profiles.
Form for updating user information.
Requires authentication to access.



Security Features

CSRF Protection:

All forms include the {% csrf_token %} tag to protect against Cross-Site Request Forgery.


Password Hashing:

Django automatically handles secure password storage using hashing algorithms.


Authentication Required:

Profile page is protected with the @login_required decorator.


Form Validation:

All forms include validation to ensure data integrity and security.



Testing Instructions
To test each feature of the authentication system:

Registration:

Navigate to /register/
Fill out the registration form with valid information
Submit the form
You should see a success message and be redirected to the login page


Login:

Navigate to /login/
Enter your username and password
Click "Login"
You should be redirected to the homepage with your username visible in the navigation


Profile Management:

While logged in, navigate to /profile/
You should see your current profile information
Update the information as desired
Submit the form
You should see a success message and your updated information


Logout:

Click "Logout" in the navigation
You should be redirected to the logout confirmation page
Navigation should now show "Login" and "Register" options instead of "Profile" and "Logout