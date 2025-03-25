# Social Media API

A Django REST Framework-based API for a social media platform, featuring user authentication and profile management.

## Features

- Custom user model with profile information
- Token-based authentication
- User registration and login
- Profile management
- Follow/unfollow functionality
- Followers and following lists

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. The API will be available at http://localhost:8000/api/

## API Endpoints

### Authentication

- **Register a new user**
  - URL: `/api/accounts/register/`
  - Method: POST
  - Request Body:
    ```json
    {
      "username": "user1",
      "email": "user1@example.com",
      "password": "securepassword123"
    }
    ```
  - Response: User data and authentication token

- **Login**
  - URL: `/api/accounts/login/`
  - Method: POST
  - Request Body:
    ```json
    {
      "username": "user1",
      "password": "securepassword123"
    }
    ```
  - Response: Authentication token

### Profile Management

- **View/Update Profile**
  - URL: `/api/accounts/profile/`
  - Method: GET (view profile) / PUT/PATCH (update profile)
  - Authentication: Token required
  - Request Body (for update):
    ```json
    {
      "bio": "My updated bio",
      "profile_picture": "image_file"
    }
    ```

### Social Network

- **Follow a User**
  - URL: `/api/accounts/follow/{user_id}/`
  - Method: POST
  - Authentication: Token required

- **Unfollow a User**
  - URL: `/api/accounts/follow/{user_id}/`
  - Method: DELETE
  - Authentication: Token required

- **View User's Followers**
  - URL: `/api/accounts/users/{user_id}/followers/`
  - Method: GET
  - Authentication: Token required

- **View User's Following**
  - URL: `/api/accounts/users/{user_id}/following/`
  - Method: GET
  - Authentication: Token required

## Authentication

The API uses token-based authentication. Include the token in the request header:

```
Authorization: Token your_auth_token_here
```

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

## License

[MIT License](LICENSE)