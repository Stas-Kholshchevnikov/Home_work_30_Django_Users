# Generated by Django 4.2 on 2023-04-10 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='member', max_length=20),
        ),
    ]