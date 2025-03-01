# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book
from django.db.models import Q

def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('app_name.can_edit', raise_exception=True)
def edit_blog_post(request, post_id):
    # Your view logic here
    pass

"book_list", "books"

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': 