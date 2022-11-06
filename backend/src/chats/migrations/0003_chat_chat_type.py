# Generated by Django 4.0 on 2022-11-01 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_chat_chat_id_alter_chat_chat_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_type',
            field=models.IntegerField(choices=[(0, 'Чат команды'), (1, 'Чат по интересам')], default=0, verbose_name='Тип чата'),
        ),
    ]
