from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=50, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    code = models.CharField(max_length=10, verbose_name='Код для верификации')
    is_active = models.BooleanField(default=False, verbose_name='Верификация')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(randint(100000, 999999))
        super().save(*args, **kwargs)


