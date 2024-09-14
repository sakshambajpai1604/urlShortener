from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class URL(models.Model):
    orignal_url=models.URLField()
    short_url=models.CharField(max_length=100)

class User(AbstractUser):
    pass