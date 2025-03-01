# Register your models here.
from django.contrib import admin
from .models import Book
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import BlogPost

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')

admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

def create_groups_and_permissions():
    content_type = ContentType.objects.get_for_model(BlogPost)
    
    can_view = Permission.objects.create(
        codename='can_view',
        name='Can view blog post',
        content_type=content_type,
    )
    can_create = Permission.objects.create(
        codename='can_create',
        name='Can create blog post',
        content_type=content_type,
    )
    can_edit = Permission.objects.create(
        codename='can_edit',
        name='Can edit blog post',
        content_type=content_type,
    )
    can_delete = Permission.objects.create(
        codename='can_delete',
        name='Can delete blog post',
        content_type=content_type,
    )

    editors, created = Group.objects.get_or_create(name='Editors')
    viewers, created = Group.objects.get_or_create(name='Viewers')
    admins, created = Group.objects.get_or_create(name='Admins')

    editors.permissions.add(can_create, can_edit)
    viewers.permissions.add(can_view)
    admins.permissions.add(can_view, can_create, can_edit, can_delete)

create_groups_and_permissions()