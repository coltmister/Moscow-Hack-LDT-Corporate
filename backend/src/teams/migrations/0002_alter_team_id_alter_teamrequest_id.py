# Generated by Django 4.0 on 2022-10-30 13:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID Пользователя'),
        ),
        migrations.AlterField(
            model_name='teamrequest',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID Заявки'),
        ),
    ]
