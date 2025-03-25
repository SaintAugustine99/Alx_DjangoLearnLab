from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Comment, Like

# Define inline classes for displaying related models
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

# Register Post with admin customizations
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'get_likes_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    inlines = [CommentInline, LikeInline]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'

# Register Comment with admin customizations
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')

# Register Like with admin customizations
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')