# Generated by Django 4.0 on 2022-11-04 18:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0017_alter_membership_membership_requester_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['-created_at'], 'verbose_name': 'Членство в команде', 'verbose_name_plural': 'Членство в команде'},
        ),
        migrations.AddField(
            model_name='membership',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 11, 4, 18, 32, 52, 180202, tzinfo=utc), verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membership',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('user', 'team'), name='user_team_unique'),
        ),
    ]
