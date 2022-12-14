# Generated by Django 4.0 on 2022-10-29 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_is_verified'),
        ('ideas', '0003_alter_ideatag_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='ideas', to='ideas.IdeaCategory', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribe_ideas', to='users.User', verbose_name='Подписчики'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='tags',
            field=models.ManyToManyField(blank=True, to='ideas.IdeaTag', verbose_name='Теги'),
        ),
    ]
