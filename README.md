

# Кастомная система аутентификации и авторизации

## Описание

Backend-приложение реализует собственную систему:

- **Аутентификации**: Token-based (не использует Django's built-in authentication)
- **Авторизации**: RBAC (Role-Based Access Control) с управлением разграничением доступа

Система полностью кастомная и не использует стандартные механизмы Django permissions и groups.

## Архитектура системы RBAC

### Модель доступа

```
User ──→ Role ──→ Permission ──→ Resource + Action
  ↑        ↑           ↑              ↑
  |        |           |              |
UserRole   |      RolePermission   Определение
           |      (связь)          прав доступа
           └── Роль пользователя
```

### Компоненты

1. **User** - пользователь системы
2. **Role** - роль (admin, user, guest и т.д.)
3. **Resource** - ресурс системы (products, orders, rbac и т.д.)
4. **Action** - действие над ресурсом (read, write, delete, assign_role)
5. **Permission** - комбинация ресурса и действия (products:read, products:write и т.д.)
6. **RolePermission** - связь роли с правами
7. **UserRole** - связь пользователя с ролью

## Реализованный функционал

### Аутентификация (Authentication)

- ✅ **Регистрация**: email, пароль, имя, фамилия, отчество
- ✅ **Вход (Login)**: по email и паролю, создание token-based сессии
- ✅ **Выход (Logout)**: аннулирование токенов пользователя
- ✅ **Мягкое удаление**: деактивация аккаунта (is_active=False)
- ✅ **Обновление профиля**: редактирование имени, фамилии, email

### Авторизация (Authorization)

- ✅ **RBAC система**: роли → права → ресурсы/действия
- ✅ **Middleware идентификации**: автоматическое определение пользователя по Bearer токену
- ✅ **HTTP статусы**:
  - `401 Unauthorized` - пользователь не аутентифицирован
  - `403 Forbidden` - пользователь аутентифицирован, но не имеет доступа
- ✅ **Admin API**: управление правами доступа (только для admin)

### Mock бизнес-ресурсы

- ✅ **Products**: CRUD операции с проверкой прав
- ✅ **Orders**: управление заказами с разграничением доступа

## Стек технологий

- Python 3.11+
- Django 4.2+
- Django REST Framework (DRF)
- SQLite (для разработки)
- PostgreSQL (рекомендуется для production)

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Применение миграций

```bash
python manage.py migrate
```

### 3. Загрузка тестовых данных

```bash
python manage.py loaddata rbac
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

Сервер доступен на `http://localhost:8000`

## API endpoints

### Аутентификация

#### Регистрация

```
POST /api/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePass123",
    "password_repeat": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael"  // optional
}
```

#### Вход

```
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "SecurePass123"
}

Response:
{
    "token": "...",
    "expires_at": "2026-01-13T12:00:00Z",
    "user": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

#### Выход

```
POST /api/auth/logout/
Authorization: Bearer {token}
```

#### Обновление профиля

```
PUT /api/auth/update/
Authorization: Bearer {token}
Content-Type: application/json

{
    "first_name": "Jane",
    "email": "newemail@example.com"
}
```

#### Удаление аккаунта

```
DELETE /api/auth/delete/
Authorization: Bearer {token}
```

### RBAC Management (Admin API)

#### Назначить права к роли

```
POST /api/rbac/permissions/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "role_name": "user",
    "resource_code": "products",
    "action_code": "read"
}
```

#### Назначить роль пользователю

```
POST /api/rbac/user-roles/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "user_id": "uuid",
    "role_name": "admin"
}
```

#### Удалить роль у пользователя

```
DELETE /api/rbac/user-roles/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "user_id": "uuid",
    "role_name": "user"
}
```

### Mock Business Resources

#### Список продуктов

```
GET /api/products/
Authorization: Bearer {token}
```

#### Деталь продукта

```
GET /api/products/{product_id}/
Authorization: Bearer {token}
```

#### Обновить продукт

```
PUT /api/products/{product_id}/
Authorization: Bearer {token}
Content-Type: application/json
```

#### Удалить продукт

```
DELETE /api/products/{product_id}/
Authorization: Bearer {token}
```

#### Список заказов

```
GET /api/orders/
Authorization: Bearer {token}
```

## Тестовые данные

После `loaddata rbac` в базе создаются:

### Роли

- **admin** - полный доступ ко всем ресурсам и действиям
- **user** - доступ на чтение и создание для products и orders
- **guest** - доступ только на чтение products

### Ресурсы

- **products** - управление продуктами
- **orders** - управление заказами
- **rbac** - управление доступом (только admin)

### Действия

- **read** - чтение
- **write** - создание/обновление
- **delete** - удаление
- **assign_role** - назначение ролей

## Проверка безопасности

✅ **Шифрование паролей**: используется Django's `make_password`
✅ **Token-based auth**: нет сессионных cookies
✅ **Валидация входных данных**: проверка обязательных полей
✅ **Обработка исключений**: правильные HTTP статусы
✅ **Защита от дублирования**: unique constraints в моделях
✅ **Мягкое удаление**: сохранение данных для аудита

## Администрирование

Django admin доступен на `/admin/` с полным управлением:

- Пользователи и токены
- Роли и права доступа
- Ресурсы и действия
- Продукты и заказы
