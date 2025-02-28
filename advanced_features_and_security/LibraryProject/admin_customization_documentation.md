# Django Admin Customization for the `Book` Model

## Steps to Register and Customize the `Book` Model in the Admin Interface

1. **Register the `Book` Model:**
   - Open `bookshelf/admin.py`.
   - Import the `Book` model and register it with the admin site:
     ```python
     from django.contrib import admin
     from .models import Book

     admin.site.register(Book)
     ```

2. **Customize the Admin Interface:**
   - Create a custom admin class for the `Book` model:
     ```python
     class BookAdmin(admin.ModelAdmin):
         list_display = ('title', 'author', 'publication_year')
         list_filter = ('author', 'publication_year')
         search_fields = ('title', 'author')
     ```
   - Register the `Book` model with the custom admin class:
     ```python
     admin.site.register(Book, BookAdmin)
     ```

3. **Verify the Admin Interface:**
   - Run the development server:
     ```bash
     python manage.py runserver
     ```
   - Log in to the Django admin panel and navigate to the `Books` section.
   - Ensure the customizations (list display, filters, and search) are working as expected.

## Expected Outcome
- The `Book` model is visible in the Django admin panel.
- The list view displays `title`, `author`, and `publication_year`.
- Filters for `author` and `publication_year` are available.
- A search bar allows searching by `title` and `author`.
