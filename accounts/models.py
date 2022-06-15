from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from .customuser import UserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class CustomUser(AbstractUser,PermissionsMixin):
    
    propic = models.ImageField(upload_to='profilepic')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address = models.TextField(max_length=500, default=None, null=True)
    city = models.CharField(max_length=200, default=None, null=True)
    state = models.CharField(max_length=200, default=None, null=True)
    pincode = models.PositiveIntegerField(default=None, null=True)

    
    # is_superuser = models.BooleanField(default=False)

    USER_TYPE_CHOICES = (
      ('patient', 'patient'),
      ('doctor', 'doctor'),
  )

    user_type = models.CharField(choices=USER_TYPE_CHOICES  ,default="None", max_length=50)

    # user_type = models.ManyToManyField(UserType)
    object = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []