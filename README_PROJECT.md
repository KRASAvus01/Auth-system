# Auth-system

Проект: система аутентификации и авторизации (Django + DRF).

## Что добавлено/улучшено

- Перенос SECRET_KEY в `.env` (см. `.env.example`).
- DRF сериализаторы для `mock_resources` (Product, Order).
- Сервисный слой: `mock_resources/services.py`.
- Views обновлены для использования ORM/сериализаторов.
- Исправлен тест `mock_resources/tests.py`.
- Добавлены Dockerfile и docker-compose.yml.
- Добавлена документация OpenAPI/Swagger (`drf-yasg`).
- Добавлен CI workflow GitHub Actions для запуска тестов.

## Быстрый запуск (локально)

1. Скопируйте `.env.example` в `.env` и заполните `SECRET_KEY`:

```bash
cp .env.example .env
# Откройте .env и задайте SECRET_KEY
```

1. Создайте и активируйте виртуальное окружение, установите зависимости:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install -r auth_system/requirements.txt
```

1. Выполните миграции и запустите сервер:

```bash
cd auth_system
python manage.py migrate
python manage.py runserver
```

1. Swagger UI доступен по: `http://127.0.0.1:8000/swagger/`

## Запуск через Docker

```bash
cp .env.example .env
docker-compose up --build
# сервис будет доступен на порту 8000
```

## CI

В репозитории добавлен workflow `.github/workflows/ci.yml`, который выполняет миграции и запускает тесты при push/pull_request в `main`.

## Как запушить в GitHub

1. Если у вас установлен Git и репозиторий ещё не создан на GitHub:

```bash
# инициализировать локально (если ещё не инициализировано)
git init
git add .
git commit -m "Initial: apply improvements (env, serializers, services, Docker, CI, Swagger, tests)"

# создать репозиторий с помощью GitHub CLI (рекомендуется)
# gh должен быть установлен и вы должны быть залогинены
gh repo create KRASAvus01/Auth-system --public --source=. --remote=origin --push
```

1. Если вы не используете `gh`, добавьте remote и запушьте:

```bash
git remote add origin https://github.com/KRASAvus01/Auth-system.git
git branch -M main
git push -u origin main
```

Если у вас включена двухфакторная аутентификация — используйте Personal Access Token при push по HTTPS или настройте SSH.

## Что можно улучшить далее

- Добавить больше тестов (сериализаторы, services, permissions).
- Добавить фикстуры/фабрики для тестов (factory_boy).
- Настроить полноценную конфигурацию для продакшн (NGINX, Gunicorn, переменные окружения для БД).

---
Если хотите, я могу сейчас помочь выполнить `git push` за вас: для этого потребуется дать доступ (PAT) или временно настроить интеграцию. Либо выполните команды выше локально — помогу при ошибках.
