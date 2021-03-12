from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

#to remove the username field and use email instead
from django.contrib.auth.models import BaseUserManager 


#<!-- user details will be stored in DB using models------------
class CustomUser(AbstractUser):
  age = models.PositiveIntegerField(null=True, blank=True)