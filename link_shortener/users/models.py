from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        unique=True,
        max_length=160,
        null=False,
        blank=False,
        error_messages={
            'unique': _('A user with that username already exists.')
        })

    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=254,
        error_messages={'unique': _('A user with that email already exists.')},
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self) -> str:
        return self.first_name
