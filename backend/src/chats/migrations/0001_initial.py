# Generated by Django 4.0 on 2022-11-01 17:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID чата')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название чата')),
                ('chat_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на чат вк')),
                ('chat_id', models.IntegerField(blank=True, null=True, verbose_name='ID чата вк')),
                ('peer_id', models.IntegerField(blank=True, null=True, verbose_name='Peer ID чата вк')),
                ('users_count', models.IntegerField(default=0, verbose_name='Количество пользователей в чате')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'ordering': ['-created_at'],
            },
        ),
    ]