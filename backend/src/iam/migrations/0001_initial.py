# Generated by Django 4.0 on 2022-10-28 00:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, default=uuid.uuid4, max_length=1024, null=True, unique=True, verbose_name='Верификационный код')),
                ('value', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Значение')),
                ('is_used', models.BooleanField(default=False, verbose_name='Код использован?')),
                ('use_until', models.DateTimeField(blank=True, null=True, verbose_name='Код действителен до')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Верификационные коды',
                'db_table': 'VerifyCode',
            },
        ),
        migrations.CreateModel(
            name='LogoutUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(blank=True, null=True, verbose_name='ID сессии')),
                ('iat_before', models.DateTimeField(verbose_name='Время выхода из системы')),
                ('logout_type', models.IntegerField(choices=[(0, 'Обновление токена'), (1, 'Выход из системы')], default=0, verbose_name='Тип выхода из системы')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Logout пользователь',
                'verbose_name_plural': 'Logout пользователи',
            },
        ),
        migrations.CreateModel(
            name='Impersonation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cookies', models.JSONField(verbose_name='Cookies')),
                ('valid_until', models.DateTimeField(verbose_name='Действителен до')),
                ('token', models.CharField(max_length=1024, unique=True, verbose_name='Токен')),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to='users.user', verbose_name='Автор запроса')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_user', to='users.user', verbose_name='Целевой пользователь')),
            ],
            options={
                'verbose_name_plural': 'Impersonation',
                'db_table': 'Impersonation',
            },
        ),
        migrations.AddIndex(
            model_name='logoutuser',
            index=models.Index(fields=['user', 'iat_before', 'logout_type'], name='iam_logoutu_user_id_addaf7_idx'),
        ),
        migrations.AddIndex(
            model_name='logoutuser',
            index=models.Index(fields=['user', 'session_id'], name='iam_logoutu_user_id_8525da_idx'),
        ),
    ]