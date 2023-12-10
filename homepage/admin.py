from atexit import register
from django.contrib import admin

from homepage.forms import BookForm
from .models import Book, CustomUser

# Register your models here.
admin.site.register(Book)

#Registered the CustomUser models so we can control it on admin page, with some configuration below
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role']  # Display these fields in the admin list view
    list_filter = ['role']  # Allow filtering by these fields
    search_fields = ['username']  # Allow searching by these fields