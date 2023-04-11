from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField("Название", max_length=200)
    lat = models.DecimalField("Латтитуда", max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField("Лонгитуда", max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class UserRole(models.TextChoices):
    MEMBER = "member", "Пользователь"
    MODERATOR = "moderator", "Модератор"
    ADMIN = "admin", "Администратор"


class User(AbstractUser):
    # first_name = models.CharField("Имя", max_length=25)
    # last_name = models.CharField("Фамилия", max_length=25)
    # username = models.CharField("Пользователь", max_length=100, unique=True)
    # password = models.CharField("Пароль", max_length=25)
    role = models.CharField(choices=UserRole.choices, max_length=20, default=UserRole.MEMBER)
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location)

    # def __str__(self):
    #     return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]
