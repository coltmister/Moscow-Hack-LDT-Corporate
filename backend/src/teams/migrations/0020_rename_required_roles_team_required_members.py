# Generated by Django 4.0 on 2022-11-05 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0019_requiredmembers_team_required_roles_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='required_roles',
            new_name='required_members',
        ),
    ]
