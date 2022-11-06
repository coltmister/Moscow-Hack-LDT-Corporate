# Generated by Django 4.0 on 2022-11-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_alter_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='vk_chat_id',
            field=models.IntegerField(blank=True, max_length=255, null=True, verbose_name='ID чата вк'),
        ),
        migrations.AddField(
            model_name='team',
            name='vk_chat_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на чат вк'),
        ),
    ]