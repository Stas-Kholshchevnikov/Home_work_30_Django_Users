from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ad(models.Model):
    name = models.CharField(max_length=1000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    is_published = models.BooleanField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to='ads_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
