# Generated by Django 4.0 on 2022-11-06 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0006_alter_chat_name'),
        ('teams', '0022_alter_team_is_looking_for_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='chat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_chat', to='chats.chat', verbose_name='Чат команды'),
        ),
    ]