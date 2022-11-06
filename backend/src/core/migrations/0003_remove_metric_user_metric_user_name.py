# Generated by Django 4.0 on 2022-11-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_metric'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metric',
            name='user',
        ),
        migrations.AddField(
            model_name='metric',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя пользователя'),
        ),
    ]
