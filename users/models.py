from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

# to remove the username field and use email instead
from django.contrib.auth.models import BaseUserManager


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class SearchResultHistoryModel(models.Model):
    searchtext = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class HandleModel(models.Model):
    handle = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now=True)

# class ClaimModel(models.Model):
#     handle = models.CharField(max_length=500)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
#     date = models.DateTimeField(auto_now=True)
