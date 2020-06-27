from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from simple_history import register

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    avatar = models.URLField(blank=True, null=True)
    isPublic = models.BooleanField(default=False)
    share_with = models.ManyToManyField(
        'Profile',
        blank=True
    )
    history = HistoricalRecords()
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='categories'
    )
    history = HistoricalRecords()
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='items'
    )
    checker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='items_checked', 
        blank=True,
        null=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

register(User)