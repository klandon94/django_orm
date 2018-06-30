from __future__ import unicode_literals
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    books = models.ManyToManyField(Book, related_name='authors')
    def __str__(self):
        return self.first_name



# b1 = Book.objects.get(id=1)...
# a1 = Book.objects.get(id=1)...

# a1.books.add(b1...)
# a1.books.remove(b1...)

# b3.authors.all()

# Book.objects.filter(authors__id=3)