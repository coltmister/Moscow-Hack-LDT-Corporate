# Generated by Django 4.0 on 2022-11-04 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_country_teamrole_university_useraddinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraddinfo',
            options={'verbose_name': 'Доп. информация о пользователе', 'verbose_name_plural': 'Доп. информация о пользователе'},
        ),
    ]