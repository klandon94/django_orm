from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name

class Book(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    uploader = models.ForeignKey(User, related_name='uploaded_books')
    liked_users = models.ManyToManyField(User, related_name='liked_books')
    def __str__(self):
        return self.name


# u1 = User.objects.get(id=1)...

# Book.objects.create(uploader=u1, name='LOTR', desc='best fantasy series ever')...
# b1 = Book.objects.first()
    # u1.uploaded_books.all()
    # b1.uploader

# b3 = Book.objects.create(uploader=u2, .....)

# u1.liked_books.add(b1,b6)...
    #b1.liked_users.all()...