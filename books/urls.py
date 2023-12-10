from django.urls import path, include
from books.views import *
app_name = 'books'

urlpatterns = [
    path("", get_books, name="get_books"),
]