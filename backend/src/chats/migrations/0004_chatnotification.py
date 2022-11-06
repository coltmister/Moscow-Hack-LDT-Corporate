# Generated by Django 4.0 on 2022-11-02 17:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_chat_chat_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatNotification',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID чата')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.chat', verbose_name='Чат')),
            ],
            options={
                'verbose_name': 'Уведомления в чатах',
                'verbose_name_plural': 'Уведомления в чатах',
                'ordering': ['-created_at'],
            },
        ),
    ]
