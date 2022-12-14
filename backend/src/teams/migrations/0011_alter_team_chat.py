# Generated by Django 4.0 on 2022-11-01 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
        ('teams', '0010_team_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='chat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.chat', verbose_name='Чат команды'),
        ),
    ]
