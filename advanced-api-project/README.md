# Advanced API Project

This project demonstrates advanced Django REST Framework usage with generic views and viewsets.

## API Endpoints

### Book Endpoints (Generic Views)

- `GET /api/books/`: List all books
- `GET /api/books/{id}/`: Retrieve a specific book by ID
- `POST /api/books/create/`: Create a new book (Authentication required)
- `PUT/PATCH /api/books/{id}/update/`: Update a book (Authentication required)
- `DELETE /api/books/{id}/delete/`: Delete a book (Authentication required)

### Book Endpoints (ViewSet Approach)

- `GET /api/books-viewset/`: List all books
- `GET /api/books-viewset/{id}/`: Retrieve a specific book
- `POST /api/books-viewset/`: Create a new book (Authentication required)
- `PUT /api/books-viewset/{id}/`: Update a book (Authentication required)
- `PATCH /api/books-viewset/{id}/`: Partially update a book (Authentication required)
- `DELETE /api/books-viewset/{id}/`: Delete a book (Authentication required)

### Authentication

- `GET /api-auth/login/`: Log in using the browsable API
- `POST /api-token-auth/`: Obtain authentication token

## Permissions

- Anonymous users can view books
- Only authenticated users can create, update, or delete books

## API Filtering, Searching, and Ordering

### Filtering Options
The API supports filtering on the following Book fields:
- `title`: Filter by book title (case-insensitive contains)
- `publication_year`: Filter by exact publication year
- `author`: Filter by author ID
- `min_year`: Filter books published on or after this year
- `max_year`: Filter books published on or before this year
- `author_name`: Filter by author name (case-insensitive contains)

## Testing the API

This project includes comprehensive test coverage for all API endpoints and functionality.

### Running the Tests

To run the test suite, use the following command:

```bash
python manage.py test api