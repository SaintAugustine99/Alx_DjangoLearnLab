# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('app_name.can_edit', raise_exception=True)
def edit_blog_post(request, post_id):
    # Your view logic here
    pass

"book_list", "books"