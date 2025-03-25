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

Documenting API Endpoints
Create a simple documentation for your API endpoints. You could create a Markdown file in your project:
markdownCopy# Posts and Comments API Documentation

## Posts

### List Posts
- **URL**: `/api/posts/`
- **Method**: GET
- **Query Parameters**:
  - `search`: Search in title and content
  - `page`: Page number for pagination
  - `page_size`: Number of results per page (max 100)
- **Response**: List of posts with pagination

### Create Post
- **URL**: `/api/posts/`
- **Method**: POST
- **Auth**: Required
- **Body**:
  ```json
  {
    "title": "Post title",
    "content": "Post content"
  }

Response: Created post object

Retrieve Post

URL: /api/posts/{id}/
Method: GET
Response: Post object with comments

Update Post

URL: /api/posts/{id}/
Method: PUT/PATCH
Auth: Required (author only)
Body: Post fields to update
Response: Updated post object

Delete Post

URL: /api/posts/{id}/
Method: DELETE
Auth: Required (author only)
Response: 204 No Content

Comments
List Comments

URL: /api/comments/
Method: GET
Query Parameters:

post: Filter by post ID
page: Page number for pagination
page_size: Number of results per page (max 100)


Response: List of comments with pagination

Create Comment

URL: /api/comments/
Method: POST
Auth: Required
Body:
jsonCopy{
  "post": 1,
  "content": "Comment content"
}

Response: Created comment object

Retrieve Comment

URL: /api/comments/{id}/
Method: GET
Response: Comment object

Update Comment

URL: /api/comments/{id}/
Method: PUT/PATCH
Auth: Required (author only)
Body: Comment fields to update
Response: Updated comment object

Delete Comment

URL: /api/comments/{id}/
Method: DELETE
Auth: Required (author only)
Response: 204 No Content

Copy
## Step 11: Test the API

You can test your API using tools like Postman, curl, or the built-in Django REST Framework browsable API. Here's an example of how to test with curl:

```bash
# List posts
curl -X GET http://localhost:8000/api/posts/

# Create a post (authenticated)
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "This is the content of my post"}'

# List comments for a specific post
curl -X GET http://localhost:8000/api/comments/?post=1
That's a step-by-step guide for creating the Post app with all the required functionality. This implementation provides:

Models for Post and Comment
Serializers for data validation and transformation
ViewSets for CRUD operations
Custom permissions for author-only editing
Pagination for handling large datasets
Filtering to search posts by title or content
URL routing with DRF routers
API documentation


Finally, let's create documentation for these new endpoints:
markdownCopy# Social Media API - Follow System and Feed

## Follow System

### Follow a User
- **URL**: `/api/accounts/follow/`
- **Method**: POST
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "user_id": 2
  }

Success Response:

Code: 200
Content: {"detail": "You are now following username."}


Error Responses:

Code: 400
Content: {"detail": "You cannot follow yourself."}
OR
Content: {"detail": "You are already following this user."}



Unfollow a User

URL: /api/accounts/unfollow/
Method: POST
Auth Required: Yes
Body:
jsonCopy{
  "user_id": 2
}

Success Response:

Code: 200
Content: {"detail": "You have unfollowed username."}


Error Response:

Code: 400
Content: {"detail": "You are not following this user."}



Get Followers

URL: /api/accounts/followers/
Method: GET
Auth Required: Yes
Response: List of users who follow the authenticated user
jsonCopy[
  {
    "id": 2,
    "username": "user2",
    "first_name": "John",
    "last_name": "Doe"
  },
  ...
]


Get Following

URL: /api/accounts/following/
Method: GET
Auth Required: Yes
Response: List of users the authenticated user follows
jsonCopy[
  {
    "id": 3,
    "username": "user3",
    "first_name": "Jane",
    "last_name": "Doe"
  },
  ...
]


Feed
Get Feed

URL: /api/posts/feed/
Method: GET
Auth Required: Yes
Query Parameters:

page: Page number for pagination
page_size: Number of results per page (max 100)


Response: List of posts from followed users, ordered by newest first
jsonCopy{
  "count": 42,
  "next": "http://example.com/api/posts/feed/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Latest post",
      "content": "This is the content",
      "author": 3,
      "author_username": "user3",
      "created_at": "2025-03-25T14:30:00Z",
      "updated_at": "2025-03-25T14:30:00Z",
      "comments": [],
      "comment_count": 0
    },
    ...
  ]
}


