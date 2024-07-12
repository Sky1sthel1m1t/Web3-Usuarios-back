from django.contrib.auth.models import User
from django.db import models


class Surtidor(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.CharField(max_length=100)
    longitud = models.CharField(max_length=100)

    users = models.ManyToManyField(
        User,
        related_name='surtidor_usuarios',
        blank=True
    )
