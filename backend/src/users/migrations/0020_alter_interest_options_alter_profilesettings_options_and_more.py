# Generated by Django 4.0 on 2022-11-01 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_profilesettings_can_be_invited_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interest',
            options={'verbose_name': 'Интерес', 'verbose_name_plural': 'Интересы'},
        ),
        migrations.AlterModelOptions(
            name='profilesettings',
            options={'verbose_name': 'Настройки профиля', 'verbose_name_plural': 'Настрйоки профиля'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'Навык', 'verbose_name_plural': 'Навыки'},
        ),
        migrations.AlterModelOptions(
            name='socialnetwork',
            options={'verbose_name': 'Социальные сети', 'verbose_name_plural': 'Социальные сети'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профили пользователей', 'verbose_name_plural': 'Профиль пользователя'},
        ),
    ]
