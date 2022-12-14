# Generated by Django 4.0 on 2022-11-04 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_useraddinfo_education_level_and_more'),
        ('teams', '0016_team_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_requester',
            field=models.IntegerField(choices=[(0, 'Автоматически'), (1, 'Пользователь'), (2, 'Команда'), (3, 'Администратор')], verbose_name='Инициатор членства'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.teamrole', verbose_name='Роль в команде'),
        ),
    ]
