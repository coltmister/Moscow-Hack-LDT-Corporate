# Generated by Django 4.0 on 2022-11-04 10:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_interest_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID страны')),
                ('name', models.CharField(max_length=255, verbose_name='Название страны')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamRole',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID роли')),
                ('name', models.CharField(max_length=255, verbose_name='Название роли')),
                ('weight', models.IntegerField(default=0, verbose_name='Вес роли')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID университета')),
                ('name', models.CharField(max_length=255, verbose_name='Название университета')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг университета')),
            ],
            options={
                'verbose_name': 'Университет',
                'verbose_name_plural': 'Университеты',
            },
        ),
        migrations.CreateModel(
            name='UserAddInfo',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID заявки')),
                ('education_speciality', models.CharField(blank=True, max_length=255, null=True, verbose_name='Специальность')),
                ('education_end_year', models.IntegerField(blank=True, null=True, verbose_name='Год окончания обучения')),
                ('employment', models.IntegerField(blank=True, choices=[(0, 'Полная занятость'), (1, 'Частичная занятость'), (2, 'Проектная работа'), (3, 'Волонтерство'), (4, 'Стажировка'), (5, 'Свой бизнес'), (6, 'Самозанятый'), (7, 'Безработный')], null=True, verbose_name='Занятость')),
                ('work_experience', models.IntegerField(blank=True, null=True, verbose_name='Опыт работы')),
                ('professional_experience', models.TextField(blank=True, null=True, verbose_name='Профессиональный опыт')),
                ('has_iar', models.BooleanField(default=False, verbose_name='Наличие РИД')),
                ('has_own_company', models.BooleanField(default=False, verbose_name='Наличие собственной компании')),
                ('hack_experience', models.IntegerField(blank=True, null=True, verbose_name='Опыт участия в хакатонах')),
                ('citizenship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.country', verbose_name='Гражданство')),
                ('education_university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.university', verbose_name='Университет')),
                ('team_role', models.ManyToManyField(blank=True, to='users.TeamRole', verbose_name='Роль в команде')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='add_info', to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Анкета пользователя',
                'verbose_name_plural': 'Анкета пользователя',
            },
        ),
    ]
