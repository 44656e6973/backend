# IdeaBoard Backend

Django REST API для доски идей. Этот README сделан как справочник для фронтенд-разработки: здесь собраны базовые URL, маршруты API, форматы запросов и ответов, правила авторизации и полезные файлы проекта.

## Быстрый Старт

Запуск через Docker из корня проекта:

```powershell
docker compose -f docker/docker-compose.yml up -d --build
```

Запуск через Docker из папки `docker/`:

```powershell
docker compose up -d --build
```

После запуска:

| Сервис | URL |
| --- | --- |
| Backend API | `http://localhost:8000` |
| API v1 | `http://localhost:8000/api/v1/` |
| Admin | `http://localhost:8000/admin/` |
| PostgreSQL с хоста | `localhost:5433` |
| Redis с хоста | `localhost:6379` |

Важно: у API включены trailing slashes. На фронтенде используй пути с `/` на конце, например `GET /api/v1/ideas/`.

## Основные Файлы

| Файл | Что внутри |
| --- | --- |
| `core/urls.py` | Корневые маршруты: admin, JWT, API v1 |
| `ideaboard/api/v1/urls.py` | Маршруты `ideas`, `tags`, `comments`, `likes`, `users/me`, register |
| `ideaboard/api/v1/views.py` | Логика API endpoints |
| `ideaboard/api/v1/serializers.py` | JSON-поля, валидация, формат ответов |
| `ideaboard/models.py` | Модели `User`, `Idea`, `Tag`, `Comments`, `Likes` |
| `ideaboard/counters.py` | Redis-счетчики лайков и комментариев |
| `ideaboard/tasks.py` | Celery-задача сброса счетчиков в PostgreSQL |
| `core/celery.py` | Инициализация Celery |
| `docker/docker-compose.yml` | PostgreSQL, Redis, backend, celery worker, celery beat |
| `docker/app.Dockerfile` | Docker image для Django и Celery |

## Авторизация

API использует JWT. Для закрытых endpoints нужно передавать заголовок:

```http
Authorization: Bearer <access_token>
```

Токены можно получить через регистрацию или логин.

## Краткая Карта API

| Метод | Путь | Доступ | Назначение |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/register/` | public | Регистрация пользователя |
| `POST` | `/api/token/` | public | Получить JWT access/refresh |
| `POST` | `/api/token/refresh/` | public | Обновить access token |
| `GET` | `/api/v1/users/me/` | auth | Получить текущего пользователя |
| `PUT` | `/api/v1/users/me/` | auth | Полностью обновить профиль |
| `PATCH` | `/api/v1/users/me/` | auth | Частично обновить профиль |
| `GET` | `/api/v1/ideas/` | public | Список идей |
| `POST` | `/api/v1/ideas/` | auth | Создать идею |
| `GET` | `/api/v1/ideas/{id}/` | public | Детали идеи |
| `PUT` | `/api/v1/ideas/{id}/` | auth | Полностью обновить идею |
| `PATCH` | `/api/v1/ideas/{id}/` | auth | Частично обновить идею |
| `DELETE` | `/api/v1/ideas/{id}/` | auth | Удалить идею |
| `GET` | `/api/v1/tags/` | public | Список тегов |
| `GET` | `/api/v1/tags/{id}/` | public | Детали тега |
| `GET` | `/api/v1/ideas/{idea_pk}/comments/` | public | Комментарии идеи |
| `POST` | `/api/v1/ideas/{idea_pk}/comments/` | auth | Создать комментарий |
| `POST` | `/api/v1/ideas/{idea_pk}/likes/` | auth | Переключить лайк текущего пользователя |
| `DELETE` | `/api/v1/ideas/{idea_pk}/likes/` | auth | Убрать лайк текущего пользователя |

## Base URL Для Frontend

Для локальной разработки:

```ts
export const API_BASE_URL = "http://localhost:8000";
export const API_V1_URL = `${API_BASE_URL}/api/v1`;
```

Пример helper для авторизованных запросов:

```ts
const headers = {
  "Content-Type": "application/json",
  Authorization: `Bearer ${accessToken}`,
};
```

Если фронтенд запускается на другом origin, например `http://localhost:5173`, CORS в проекте пока не настроен. В dev-режиме можно использовать proxy на фронтенде или добавить `django-cors-headers` на backend.

## Auth Endpoints

### Регистрация

`POST /api/v1/auth/register/`

Body:

```json
{
  "username": "denis",
  "email": "denis@example.com",
  "password": "strong-password-123",
  "password_confirm": "strong-password-123"
}
```

Response `201`:

```json
{
  "user": {
    "id": 1,
    "username": "denis",
    "email": "denis@example.com",
    "avatar_URL": null,
    "created_at": "2026-05-27T10:00:00Z"
  },
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Валидация:

| Поле | Правило |
| --- | --- |
| `username` | Обязательное, уникальное |
| `email` | Обязательное, уникальное |
| `password` | Проверяется Django password validators |
| `password_confirm` | Должен совпадать с `password` |

### Логин

`POST /api/token/`

Body:

```json
{
  "username": "denis",
  "password": "strong-password-123"
}
```

Response `200`:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Обновить Access Token

`POST /api/token/refresh/`

Body:

```json
{
  "refresh": "<refresh_token>"
}
```

Response `200`:

```json
{
  "access": "<new_access_token>"
}
```

В настройках включен refresh rotation, поэтому response может также содержать новый `refresh`.

## User Endpoints

### Текущий Пользователь

`GET /api/v1/users/me/`

Headers:

```http
Authorization: Bearer <access_token>
```

Response `200`:

```json
{
  "id": 1,
  "username": "denis",
  "email": "denis@example.com",
  "avatar_URL": "https://example.com/avatar.png",
  "created_at": "2026-05-27T10:00:00Z"
}
```

### Обновить Профиль

`PATCH /api/v1/users/me/`

Body:

```json
{
  "avatar_URL": "https://example.com/new-avatar.png"
}
```

Доступные поля для изменения:

| Поле | Тип | Примечание |
| --- | --- | --- |
| `username` | string | Должен быть уникальным |
| `email` | string | Должен быть уникальным |
| `avatar_URL` | string/null | URL аватара |

## Idea Endpoints

### Поля Идеи

Response-объект идеи:

```json
{
  "id": 1,
  "title": "New idea",
  "description": "Long idea description",
  "status": "open",
  "created_at": "2026-05-27T10:00:00Z",
  "updated_at": "2026-05-27T10:00:00Z",
  "cover_image_URL": "https://example.com/cover.png",
  "likes_count": 3,
  "comments_count": 5,
  "author": {
    "id": 1,
    "username": "denis",
    "email": "denis@example.com",
    "avatar_URL": null,
    "created_at": "2026-05-27T10:00:00Z"
  },
  "tags": [
    {
      "id": 1,
      "name": "startup"
    }
  ]
}
```

Поля для создания/обновления:

| Поле | Тип | Обязательное | Примечание |
| --- | --- | --- | --- |
| `title` | string | да | 5-100 символов по текущей валидации |
| `description` | string | да | 10-2000 символов |
| `status` | string | нет | Если отправляешь, допустимо `open` или `closed` |
| `cover_image_URL` | string/null | нет | URL обложки |

Read-only поля:

| Поле | Откуда берется |
| --- | --- |
| `id` | PostgreSQL |
| `author` | Текущий JWT-пользователь |
| `created_at` | PostgreSQL |
| `updated_at` | PostgreSQL |
| `likes_count` | PostgreSQL + свежая Redis-дельта |
| `comments_count` | PostgreSQL + свежая Redis-дельта |
| `tags` | Сейчас сериализатор отдает теги только на чтение |

### Список Идей

`GET /api/v1/ideas/`

Доступ: public.

Response `200`:

```json
[
  {
    "id": 1,
    "title": "New idea",
    "description": "Long idea description",
    "status": "open",
    "created_at": "2026-05-27T10:00:00Z",
    "updated_at": "2026-05-27T10:00:00Z",
    "cover_image_URL": null,
    "likes_count": 0,
    "comments_count": 0,
    "author": {
      "id": 1,
      "username": "denis",
      "email": "denis@example.com",
      "avatar_URL": null,
      "created_at": "2026-05-27T10:00:00Z"
    },
    "tags": []
  }
]
```

### Детали Идеи

`GET /api/v1/ideas/{id}/`

Доступ: public.

Пример:

```http
GET /api/v1/ideas/1/
```

### Создать Идею

`POST /api/v1/ideas/`

Доступ: auth.

Body:

```json
{
  "title": "New idea",
  "description": "Long idea description",
  "status": "open",
  "cover_image_URL": "https://example.com/cover.png"
}
```

Response `201`: объект идеи.

Заметка для frontend: поле `tags` сейчас read-only в `IdeaSerializer`, поэтому отправка `"tags": [1, 2]` не привяжет теги к идее без доработки backend.

### Обновить Идею

`PATCH /api/v1/ideas/{id}/`

Доступ: auth.

Body:

```json
{
  "status": "closed"
}
```

Также доступен `PUT /api/v1/ideas/{id}/` для полной замены объекта.

Текущий backend требует только аутентификацию для изменения идеи. Проверка владельца идеи в `IdeaViewSet` сейчас не подключена.

### Удалить Идею

`DELETE /api/v1/ideas/{id}/`

Доступ: auth.

Response `204`: без тела.

## Tag Endpoints

Теги сейчас доступны только на чтение через `ReadOnlyModelViewSet`.

### Список Тегов

`GET /api/v1/tags/`

Доступ: public.

Response `200`:

```json
[
  {
    "id": 1,
    "name": "startup"
  },
  {
    "id": 2,
    "name": "design"
  }
]
```

### Детали Тега

`GET /api/v1/tags/{id}/`

Доступ: public.

Response `200`:

```json
{
  "id": 1,
  "name": "startup"
}
```

Недоступно сейчас:

| Метод | Путь | Причина |
| --- | --- | --- |
| `POST` | `/api/v1/tags/` | ViewSet read-only |
| `PATCH` | `/api/v1/tags/{id}/` | ViewSet read-only |
| `DELETE` | `/api/v1/tags/{id}/` | ViewSet read-only |

## Comment Endpoints

### Поля Комментария

Response-объект комментария:

```json
{
  "id": 1,
  "content": "Nice idea!",
  "created_at": "2026-05-27T10:00:00Z",
  "author": {
    "id": 1,
    "username": "denis",
    "email": "denis@example.com",
    "avatar_URL": null,
    "created_at": "2026-05-27T10:00:00Z"
  },
  "idea": 1
}
```

### Комментарии Идеи

`GET /api/v1/ideas/{idea_pk}/comments/`

Доступ: public.

Пример:

```http
GET /api/v1/ideas/1/comments/
```

Response `200`:

```json
[
  {
    "id": 1,
    "content": "Nice idea!",
    "created_at": "2026-05-27T10:00:00Z",
    "author": {
      "id": 1,
      "username": "denis",
      "email": "denis@example.com",
      "avatar_URL": null,
      "created_at": "2026-05-27T10:00:00Z"
    },
    "idea": 1
  }
]
```

Сортировка: новые комментарии первыми.

### Создать Комментарий

`POST /api/v1/ideas/{idea_pk}/comments/`

Доступ: auth.

Body:

```json
{
  "content": "Nice idea!"
}
```

Валидация:

| Поле | Правило |
| --- | --- |
| `content` | Обязательное, не пустое, максимум 500 символов |

Response `201`: объект комментария.

После создания комментария `comments_count` у идеи увеличивается через Redis и позже сохраняется в PostgreSQL через Celery.

Удаление комментария в `CommentViewSet` частично реализовано, но URL для `DELETE` сейчас не подключен в `ideaboard/api/v1/urls.py`.

## Like Endpoints

Лайк привязан к текущему JWT-пользователю и идее. Один пользователь может лайкнуть одну идею только один раз.

### Переключить Лайк

`POST /api/v1/ideas/{idea_pk}/likes/`

Доступ: auth.

Body не нужен.

Если лайка еще не было, response `201`:

```json
{
  "status": "liked",
  "like_id": 10
}
```

Если лайк уже был, endpoint удалит его и вернет response `200`:

```json
{
  "status": "unliked"
}
```

После изменения лайка `likes_count` у идеи меняется через Redis и позже сохраняется в PostgreSQL через Celery.

### Убрать Лайк

`DELETE /api/v1/ideas/{idea_pk}/likes/`

Доступ: auth.

Если лайк найден, response `200`:

```json
{
  "status": "unliked"
}
```

Если лайка нет, response `404`:

```json
{
  "detail": "Like not found"
}
```

## Счетчики Лайков И Комментариев

Frontend читает счетчики прямо из объекта идеи:

```json
{
  "likes_count": 3,
  "comments_count": 5
}
```

Как это работает внутри:

| Шаг | Что происходит |
| --- | --- |
| 1 | `Like` или `Comment` сразу сохраняется в PostgreSQL |
| 2 | После commit backend пишет дельту счетчика в Redis |
| 3 | При чтении идеи API показывает `PostgreSQL count + Redis delta` |
| 4 | Celery beat раз в 60 секунд запускает задачу |
| 5 | Celery worker переносит накопленные дельты из Redis в PostgreSQL |

Фронтенду не нужно отдельно ходить в Redis или Celery. Достаточно перечитать идею или список идей.

## HTTP Статусы

| Код | Когда ожидать |
| --- | --- |
| `200` | Успешный GET/PATCH/PUT/DELETE с телом ответа |
| `201` | Успешное создание пользователя, идеи, комментария или нового лайка |
| `204` | Успешное удаление идеи |
| `400` | Ошибка валидации body |
| `401` | Нет JWT или token неверный |
| `403` | Доступ запрещен |
| `404` | Объект не найден |

Пример ошибки валидации:

```json
{
  "title": [
    "Title must be at least 5 characters long."
  ]
}
```
## Локальная Разработка Без Docker

Установить зависимости:

```powershell
uv sync
```

Применить миграции:

```powershell
uv run python manage.py migrate
```

Запустить backend:

```powershell
uv run python manage.py runserver
```

Запустить Celery worker:

```powershell
uv run celery -A core worker --loglevel=info
```

Запустить Celery beat:

```powershell
uv run celery -A core beat --loglevel=info
```

Для локального запуска без Docker нужен запущенный PostgreSQL и Redis, а переменные подключения задаются в `.env`.

## Переменные Окружения

Пример `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=ideaboard_db
DB_USER=ideaboard_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

В Docker контейнеры используют:

| Переменная | Значение по умолчанию |
| --- | --- |
| `DB_NAME` | `ideaboard_db` |
| `DB_USER` | `ideaboard_user` |
| `DB_PASSWORD` | `secure_password` |
| `DB_HOST` | `db` |
| `DB_PORT` | `5432` |
| `REDIS_URL` | `redis://redis:6379/0` |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | `redis://redis:6379/0` |

## Проверки

Запуск тестов:

```powershell
uv run pytest
```

