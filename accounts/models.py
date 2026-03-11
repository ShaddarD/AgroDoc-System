from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    company_name = models.CharField('Наименование компании', max_length=500, blank=True)
    inn = models.CharField('ИНН', max_length=12, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'
