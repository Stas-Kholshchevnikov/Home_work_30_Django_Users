from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Ad(models.Model):
    name = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()
