# Добро пожаловать

## Данный репозиторий содержит backend составляющую проекта в рамках конкурса "Лидеры цифровой трансформации 2022"

## Стек

- Python 3.10 +
- Django 4.0
- Django REST Framework 3.13.1
- PostgreSQL 14.1
- Gunicorn 20.1.0
- Celery 5.2.7
- Docker
- Docker Compose

## Запуск

Для запуска проекта необходимо указать переменные окружения в файле `src/settings/.dev.env`:

```bash
# .env
PRODUCTION=True
DEBUG=False
# Разрешенные хосты
ALLOWED_HOSTS=
# Cors headers
CORS_ALLOWED_ORIGIN_REGEXES=
# Данные для подключения к Keycloak (SSO-провайдер)
CLIENT_ID=
CLIENT_SECRET=
MASTER_REALM_ENDPOINT=https://{HOST}/auth/realms/dpir
USER_INFO_ENDPOINT=https://{HOST}/auth/realms/{REALM}/protocol/openid-connect/userinfo
AUTHORIZATION_ENDPOINT=https://{HOST}/auth/realms/{REALM}/protocol/openid-connect/token
USERS_ENDPOINT=https://{HOST}/auth/admin/realms/{REALM}/users
REDIRECT_URI=https://{HOST}/api/v1/iam/auth/login/
ADMIN_URL=https://{HOST}/auth/admin/realms/{REALM}
ACCOUNT_SESSION_URL=https://{HOST}/auth/realms/{REALM}/account/sessions
ADMIN_SESSION_URL=https://{HOST}/auth/admin/realms/{REALM}/sessions
END_SESSION_ENDPOINT=https://{HOST}/auth/realms/{REALM}/protocol/openid-connect/logout
JWT_HASH=RS256
# Доп. данные для авторизации
FRONT_URL=https://{FRONT_LOGIN_URL}
FRONT_LOGIN_URL=https://{FRONT_URL}/login
IMPERSONATION_URL=https://{FRONT_URL}/api/v1/iam/impersonation/redirect/
# Токен для отправки сообщений в Telegram
TELEGRAM_BOT_TOKEN=
# Данные для подключения к S3-хранилищу для хранения аватаров пользователей
S3_SERVER=
S3_ACCESS_KEY=
S3_SECRET_KEY=
# Данные для подкючению к боту ВК
VK_ACCESS_TOKEN=
VK_GROUP_ID=
VK_SECRET_KEY=
VK_BOT_NAME=
# Данные для подключению к почте (SMTP)
EMAIL_HOST=
EMAIL_PORT=465
EMAIL_ADDRESS=
EMAIL_PASSWORD=
````

Запуск проекта осуществляется командой:

```bash
ln -s src/settings/.dev.env .env
chmod -R 777 ./redis/redis-data
docker-compose up -d --build python
docker-compose exec python python manage.py migrate
docker-compose exec python python manage.py createsuperuser
docker-compose exec python python manage.py collectstatic
docker-compose exec python python manage.py loaddata ./settings/fixtures/users.interest.json
docker-compose down && docker-compose up -d
```

---
Отдельно следует создать бакеты на S3-сервере для хранения аватарок пользователей и файлов с данными:

Бакеты должны иметь следующие названия:

* idea-files
* users-avatars
* post-files
  Бакеты должны быть доступны для чтения публично и для записи с помощью ключей доступа, указанных в переменных
  окружения `S3_ACCESS_KEY` и `S3_SECRET_KEY`

## Разработчики Backend

* Даниил
    * TG: http://t.me/MartinOrlov
* Ярослав
    * TG: https://t.me/coltadmin
* 

