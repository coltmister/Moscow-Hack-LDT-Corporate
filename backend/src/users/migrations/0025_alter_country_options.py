# Generated by Django 4.0 on 2022-11-04 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_useraddinfo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
    ]
