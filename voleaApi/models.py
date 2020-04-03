from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from simple_history import register

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    avatar = models.URLField(blank=True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.user.username

        
class List(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    sharedWith = models.ManyToManyField(
        Profile, 
        'user_list',
        'sharedWith',
        blank=True
    )
    isPublic = models.BooleanField(
        default=False
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    list = models.ForeignKey(List, related_name='items', on_delete = models.CASCADE)
    owner = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='owner'
    )
    checker = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='checker', 
        blank=True,
        null=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

register(User)