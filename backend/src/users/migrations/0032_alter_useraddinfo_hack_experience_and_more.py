# Generated by Django 4.0 on 2022-11-06 17:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_country_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddinfo',
            name='hack_experience',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(60)], verbose_name='Опыт участия в хакатонах'),
        ),
        migrations.AlterField(
            model_name='useraddinfo',
            name='work_experience',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(60)], verbose_name='Опыт работы'),
        ),
    ]
