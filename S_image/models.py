from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class EncryptedHistory(models.Model):
    user = models.CharField(max_length=100)
    E_image = models.ImageField(upload_to='E_image')
    E_date = models.DateField(default=now)