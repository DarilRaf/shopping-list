from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    published_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.TextField(null=True, blank=True)
    ratings_avg = models.FloatField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    isbn10 = models.TextField(null=True, blank=True)
    isbn13 = models.TextField(null=True, blank=True)
    