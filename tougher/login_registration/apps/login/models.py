from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime, timedelta
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')

class UserManager(models.Manager):
    def register_validator(self, postdata):
        errors = {}
        if not postdata['first_name']:
            errors['first_name'] = 'Please enter your first name'
        elif len(postdata['first_name']) <= 2 or not postdata['first_name'].isalpha():
            errors['first_name'] = 'Must only be letters and more than 2 characters'

        if not postdata['last_name']:
            errors['last_name'] = 'Please enter your last name'
        elif len(postdata['last_name']) <= 2 or not postdata['last_name'].isalpha():
            errors['last_name'] = 'Must only be letters and more than 2 characters'

        if not postdata['email']:
            errors['email'] = 'Please enter your email'
        elif not EMAIL_REGEX.match(postdata['email']):
            errors['email'] = 'Invalid email address'

        if not postdata['password']:
            errors['password'] = 'Please enter a password'
        elif len(postdata['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if not postdata['confirm_password']:
            errors['confirm_password'] = 'Please confirm your password'
        elif postdata['confirm_password'] != postdata['password']:
            errors['confirm_password'] = 'Passwords do not match'

        if not postdata['birthday']:
            errors['birthday'] = 'Please enter your birth date'
        elif (datetime.strptime(str(date.today()), '%Y-%m-%d') - datetime.strptime(postdata['birthday'], '%m/%d/%Y'))//timedelta(days=1) < (13*365.2):
            errors['birthday'] = 'You must be at least 13 years old to register'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    objects = UserManager()
    def __repr__(self):
        return "<User: {} {}>".format(self.first_name, self.last_name)

