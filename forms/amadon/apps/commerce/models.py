from __future__ import unicode_literals
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return "<Product {}: ${}>".format(self.name, self.price)