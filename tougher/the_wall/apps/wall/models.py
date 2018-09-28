from __future__ import unicode_literals
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')

class UserManager(models.Manager):
    def login(self, data):
        result = {
            'messages': [],
            'user': None
        }
        if not data['login_email'] or not data['login_password']:
            result['messages'].append("Please fill out all fields")
        elif User.objects.filter(email=data['login_email']):
            result['user'] = User.objects.get(email=data['login_email'])
            if bcrypt.checkpw(data['login_password'].encode(), result['user'].password.encode()):
                return result
            else:
                result['messages'].append("You could not be logged in...")
        else:
            result['messages'].append("You have not registered")
        return result

    def register(self, data):
        result = {
            'messages': [],
            'user': None
        }
        if not data['first_name']:
            result['messages'].append("Please enter a first name")

        if not data['last_name']:
            result['messages'].append("Please enter a last name")

        if not data['register_email']:
            result['messages'].append("Please enter an email")
        elif not EMAIL_REGEX.match(data['register_email']):
            result['messages'].append("Invalid email address")
        
        if not data['register_password']:
            result['messages'].append("Please enter a password")
        elif len(data['register_password']) < 8:
            result['messages'].append("Password must be at least 8 characters")
        
        if not data['confirm_password']:
            result['messages'].append('Please confirm your password')
        elif data['confirm_password'] != data['register_password']:
            result['messages'].append('Passwords do not match')

        if not result['messages']:
            hasher = bcrypt.hashpw(data['register_password'].encode(), bcrypt.gensalt())
            result['user'] = User.objects.create(first_name = data['first_name'], last_name = data['last_name'], email = data['register_email'], password = hasher)

        return result

class MessageManager(models.Manager):
    def postMessage(self, user, msg):
        Message.objects.create(messenger=user, content=msg)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User: {}, {}>".format(self.first_name, self.email)

class Message(models.Model): 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    messenger = models.ForeignKey(User, related_name='messages')
    objects = MessageManager()
    def __str__(self):
        return self.content

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(User, related_name='usercomments')
    whichmessage = models.ForeignKey(Message, related_name='msgcomments')
    def __str__(self):
        return self.content