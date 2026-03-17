# TMS Online Courses

Backend-приложение для платформы онлайн-курсов.
Проект реализует REST API для управления курсами, уроками, пользователями и процессом обучения.

Приложение разработано на **Django + Django REST Framework** и демонстрирует практическое применение архитектуры backend-сервисов, тестирования и контейнеризации.

---

# Основные возможности

Платформа позволяет:

* регистрировать пользователей
* управлять курсами
* добавлять уроки
* отслеживать прогресс обучения
* оставлять отзывы
* получать уведомления

---

# Архитектура проекта

Проект построен по **модульной архитектуре Django apps**.

```
tms_online_courses
│
├── config/                # настройки проекта
│
├── users/                 # пользователи и авторизация
│
├── courses/               # курсы
│
├── lessons/               # уроки внутри курсов
│
├── reviews/               # отзывы пользователей
│
├── notifications/         # система уведомлений
│
├── providers/             # интеграции (Redis, внешние сервисы)
│
├── utils/                 # вспомогательные функции
│
├── tests/                 # тесты проекта
│
├── docker-compose.yml     # инфраструктура
├── pyproject.toml         # зависимости Poetry
└── manage.py
```

---

# Технологический стек

Backend:

* Python
* Django
* Django REST Framework

База данных и инфраструктура:

* PostgreSQL
* Redis
* Memcached

DevOps:

* Docker
* Docker Compose
* Poetry

Тестирование:

* Pytest
* Factory Boy

---

# Модели системы

Основные сущности платформы:

### User

Пользователь системы.

Поля:

* id
* email
* password
* role
* date_joined

---

### Course

Курс, доступный на платформе.

Поля:

* id
* title
* description
* author
* created_at

Связи:

* один курс содержит несколько уроков

---

### Lesson

Отдельный урок курса.

Поля:

* id
* title
* content
* course
* order

---

### Review

Отзыв пользователя о курсе.

Поля:

* id
* user
* course
* rating
* comment

---

### Notification

Система уведомлений пользователей.

Поля:

* id
* user
* message
* created_at
* is_read

---

# REST API

## Аутентификация

```
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
```

---

## Пользователи

```
GET /api/users/
GET /api/users/{id}/
PUT /api/users/{id}/
```

---

## Курсы

```
GET /api/courses/
POST /api/courses/
GET /api/courses/{id}/
PUT /api/courses/{id}/
DELETE /api/courses/{id}/
```

---

## Уроки

```
GET /api/lessons/
POST /api/lessons/
GET /api/lessons/{id}/
PUT /api/lessons/{id}/
DELETE /api/lessons/{id}/
```

---

## Отзывы

```
GET /api/reviews/
POST /api/reviews/
```

---

# Запуск проекта

## Установка зависимостей

Проект использует **Poetry**.

```bash
poetry install
poetry shell
```

---

# Миграции

```
python manage.py migrate
```

---

# Создание суперпользователя

```
python manage.py createsuperuser
```

---

# Запуск сервера

```
python manage.py runserver
```

Приложение будет доступно:

```
http://127.0.0.1:8000
```

---

# Docker

Docker используется для запуска инфраструктурных сервисов.

## Запуск

```
docker-compose up -d
```

Будут запущены:

* PostgreSQL
* Redis
* Memcached

Проверка контейнеров:

```
docker-compose ps
```

Остановка:

```
docker-compose down
```

---

# Тестирование

Проект использует **pytest**.

Запуск тестов:

```
pytest
```

Тесты покрывают:

* модели
* сериализаторы
* API endpoints
* бизнес-логику

---

# Назначение проекта

Учебный backend-проект для практики:

* разработки REST API
* архитектуры Django приложений
* работы с Redis
* контейнеризации через Docker
* написания тестов
