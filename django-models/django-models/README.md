# django-models

This project demonstrates the use of Django's Object-Relational Mapping (ORM) capabilities by showcasing complex relationships between entities using ForeignKey, ManyToMany, and OneToOne fields.

## Project Structure

- **django_models/**: Contains the main Django project files.
  - **settings.py**: Configuration settings for the Django project.
  - **urls.py**: URL routing for the project.
  - **wsgi.py**: Entry point for WSGI-compatible web servers.
  - **asgi.py**: Entry point for ASGI-compatible web servers.

- **relationship_app/**: Contains the application that defines complex models.
  - **models.py**: Defines the following models:
    - **Author**: Represents an author with a name.
    - **Book**: Represents a book with a title and a ForeignKey to Author.
    - **Library**: Represents a library with a name and a ManyToManyField to Book.
    - **Librarian**: Represents a librarian with a name and a OneToOneField to Library.
  - **query_samples.py**: Contains sample queries to demonstrate the relationships:
    - Query to retrieve all books by a specific author.
    - Query to list all books in a library.
    - Query to retrieve the librarian for a library.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd django-models
   ```

2. **Install dependencies**:
   Ensure you have Python and Django installed. You can install Django using pip:
   ```
   pip install django
   ```

3. **Run migrations**:
   To create the necessary database tables, run:
   ```
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

4. **Run the development server**:
   Start the server with:
   ```
   python manage.py runserver
   ```

5. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000/` to view the application.

## Purpose

The purpose of this project is to master Django's ORM capabilities by effectively modeling complex data relationships, which is essential for building robust web applications.