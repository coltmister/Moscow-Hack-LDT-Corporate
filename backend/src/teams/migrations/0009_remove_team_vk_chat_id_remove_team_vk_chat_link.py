# Generated by Django 4.0 on 2022-11-01 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_team_vk_chat_id_team_vk_chat_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='vk_chat_id',
        ),
        migrations.RemoveField(
            model_name='team',
            name='vk_chat_link',
        ),
    ]
