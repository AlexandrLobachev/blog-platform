#  Blog-platform

## Описание

API для блог-платформы.

## Автор:

[Александр Лобачев](https://github.com/AlexandrLobachev/)

## Технологии используемые в проекте:

Python, Django, DRF, Nginx, Docker, Gunicorn, PostgreSQL

## Как запустить проект локально:

Для запуска на Windows вам потребуеться установить Docker и WSL.
Скачать можно с официального сайта и там же есть инструкции.

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:AlexandrLobachev/blog-platform.git
```
```
cd blog-platform
```
Создать файл .env и заполнить его(пример заполнения можно взять ниже):
```
POSTGRES_DB=blog_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY = 'django-insecure-(4f*^&o%pql#jpm$$*ba907w658@6_mhw7u_dt=1@yj=!f-e*-'
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1 localhost
```
Создать образы и запустить контейнеры командой:
```
docker compose up
```
Выполните миграции
```
docker compose exec backend python manage.py migrate
```
Соберите статические файлы
```
docker compose exec backend python manage.py collectstatic
```
Скопируйте статические файлы
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
Создать суперпользователя
```
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Проект доступен по адресу:
```
http://127.0.0.1:8000/
```

Динамическая документация доступна по адресу:
```
http://127.0.0.1:8000/swagger/
```

## Тестирование через Postman:
В директории postman-collection сохранена коллекция тестовых запросов для API.

## Примеры запросов:

### Создание пользователя: 
POST http://127.0.0.1:8000/api/users/

```
{
    "email": "user@user.com",
    "username": "user",
    "password": "Zxc123654"
}
```
### Создание получение токена для пользователя: 
POST http://127.0.0.1:8000/api/auth/jwt/create/

```
{
    "username": "user",
    "password": "Zxc123654"
}
```
Из ответа берем "access" token и далее передаем с запросами.


### Создание поста
Создание поста доступно только зарегистрированным пользователям: 

POST http://127.0.0.1:8000/api/posts/

Поле "status" не являеться обязательным, по умолчанию "draft". Возможные варианты "published" и "draft".

Если при создании поста поставить дату более текущей, то посту будет виден други пользователям только при наступлении даты, 
посты со статусом "черновик" не видны другим пользователям.

```
{
    "title": "Заголовок",
    "text": "Текст поста",
    "pub_date": "2024-04-18",
    "status": "published"
}
```
пример ответа:
```
{
    "id": 2,
    "title": "Заголовок",
    "text": "Текст поста",
    "pub_date": "2024-04-18",
    "author": "user",
    "status": "published"
}
```
### Получение списка всех постов:

Эндпойнт GET http://127.0.0.1:8000/api/posts/ доступен всем пользователям.

Авторизованный пользователь видит опубликованные посты всех авторов с датой менее текущей и все 
свои(не опубликованные и с отложенной публикацией).

### Получение списка всех постов текущего пользователя:

Все посты(включая отложенные посты и черновики) ТОЛЬКО ТЕКУЩЕГО пользователя доступны в эндпойнте:

GET http://127.0.0.1:8000/api/myposts/

### Фильтрация постов:
Доступна фильтрация по статусу и по дате.

Примеры запросов:

фильтрация по дате и статусу:

http://127.0.0.1:8000/api/posts/?pub_date=2024-04-19&status=draft

фильтрация по дате:

http://127.0.0.1:8000/api/posts/?pub_date=2024-04-19

фильтрация по статусу:

http://127.0.0.1:8000/api/posts/?status=draft

### Получение поста

GET http://127.0.0.1:8000/api/posts/{id}/ 

Пример ответа
```
{
    "id": 2,
    "title": "Заголовок",
    "text": "Текст поста",
    "pub_date": "2024-04-18",
    "author": "user",
    "status": "published"
}
```
### Редактирование поста:
Редактирование и удаление поста доступно только автору или администратору.

PATCH http://127.0.0.1:8000/api/posts/{id}/ 

```
{
    "title": "Другой заголовок"
}
```
Пример ответа:
```
{
    "id": 2,
    "title": "Другой заголовок",
    "text": "Текст поста",
    "pub_date": "2024-04-18",
    "author": "user",
    "status": "published"
}
```
### Удаление поста:

DELETE http://127.0.0.1:8000/api/posts/{id}/ 

### Комментарии:
### Получение списка комментариев:
GET http://127.0.0.1:8000/api/posts/{post_id}/comments/

### Получение списка комментариев:
GET http://127.0.0.1:8000/api/posts/{post_id}/comments/

### Создание комментария:
Создание поста доступно только зарегистрированным пользователям

POST http://127.0.0.1:8000/api/posts/{post_id}/comments/
```
{
    "text": "Текст комментария."
}
```
### Изменение комментария:
Редактирование и удаление комментария доступно только автору или администратору.

PATCH http://127.0.0.1:8000/api/posts/{post_id}/comments/{comment_id}/
```
{
    "text": "Измененный текст комментария.",
}
```
### Удаление комментария
DELETE http://127.0.0.1:8000/api/posts/{post_id}/comments/{comment_id}/
