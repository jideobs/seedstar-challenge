from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=60, unique=True)
    date_entered = models.DateTimeField(auto_now=True)
    date_last_modified = models.DateTimeField(auto_now_add=True)
