from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'timestamp', 'read')
    list_filter = ('read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb', 'description')
    raw_id_fields = ('recipient', 'actor')
    date_hierarchy = 'timestamp'