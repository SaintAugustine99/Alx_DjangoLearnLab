# Django Models Project

This project demonstrates the use of Django's Object-Relational Mapping (ORM) capabilities by creating a set of models that showcase complex relationships between entities. The primary focus is on utilizing ForeignKey, ManyToMany, and OneToOne relationships.

## Project Structure

```
django-models
├── django_models
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── relationship_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── query_samples.py
├── manage.py
└── README.md
```

## Setup Instructions

1. **Clone the Repository:**
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory:**
   ```
   cd django-models
   ```

3. **Create a Virtual Environment:**
   It is recommended to create a virtual environment for the project:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install Dependencies:**
   Install Django using pip:
   ```
   pip install django
   ```

5. **Run Migrations:**
   Apply the migrations to set up the database:
   ```
   python manage.py makemigrations relationship_app
   python manage.py migrate
   ```

6. **Run the Development Server:**
   Start the Django development server:
   ```
   python manage.py runserver
   ```

## Models Overview

- **Author**: Represents an author with a name.
- **Book**: Represents a book with a title and a foreign key to the author.
- **Library**: Represents a library with a name and a many-to-many relationship with books.
- **Librarian**: Represents a librarian with a name and a one-to-one relationship with a library.

## Sample Queries

The `query_samples.py` script contains examples of how to query the database:
- Query all books by a specific author.
- List all books in a library.
- Retrieve the librarian for a library.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.