# Generated by Django 4.0 on 2022-11-01 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='chat_id',
            field=models.IntegerField(default=None, unique=True, verbose_name='ID чата вк'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='chat_link',
            field=models.URLField(default=None, verbose_name='Ссылка на чат вк'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chat',
            name='peer_id',
            field=models.IntegerField(default=None, unique=True, verbose_name='Peer ID чата вк'),
            preserve_default=False,
        ),
    ]