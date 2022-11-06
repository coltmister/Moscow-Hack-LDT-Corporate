# Generated by Django 4.0 on 2022-11-06 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0013_alter_ideainformation_options_alter_idea_status_and_more'),
        ('teams', '0020_rename_required_roles_team_required_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='idea',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='ideas.idea', verbose_name='Идея'),
        ),
    ]