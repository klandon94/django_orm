from __future__ import unicode_literals
from django.db import models

class Dojo(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    desc = models.TextField()
    def __repr__(self):
        return "<Dojo object: {}>".format(self.name)

class Ninja(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dojo = models.ForeignKey(Dojo, related_name='ninjas')
    def __repr__(self):
        return "<Ninja object: {} {}>".format(self.first_name, self.last_name)