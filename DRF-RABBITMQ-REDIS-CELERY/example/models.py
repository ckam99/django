from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    published = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, models.CASCADE, null=True, blank=True, related_name='books')
    category = models.ForeignKey(
        Category, models.SET_NULL, null=True, blank=True, related_name='categories')
    tags = models.ManyToManyField(
        Tag, related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
