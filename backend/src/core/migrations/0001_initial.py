# Generated by Django 4.0 on 2022-10-28 00:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID Черновика')),
                ('key', models.TextField(verbose_name='Ключ')),
                ('expiration_date', models.DateTimeField(verbose_name='Время истечения срока действия черновика')),
                ('data', models.JSONField(verbose_name='Данные черновика')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Черновик',
                'verbose_name_plural': 'Черновики',
            },
        ),
    ]