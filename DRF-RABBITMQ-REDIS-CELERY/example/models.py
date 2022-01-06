from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    published = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, models.CASCADE, null=True, blank=True, related_name='books')
