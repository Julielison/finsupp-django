from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(
        'endereço de e-mail',
        unique=True,
        error_messages={
            'unique': 'Já existe um usuário cadastrado com este e-mail.',
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name() or self.email

    def get_short_name(self):
        return self.first_name
