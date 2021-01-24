from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listing(models.Model):
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=64, blank = True)
    image = models.URLField(default=None,blank=True,null=True)
    active =  models.BooleanField()

class Bid(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()
    
class Watchlist(models.Model):
    user = models.CharField(max_length = 64)
    listingid = models.IntegerField()