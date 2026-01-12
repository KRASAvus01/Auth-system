# Примеры использования API

## Базовый URL
```
http://localhost:8000
```

## Аутентификация

### 1. Регистрация нового пользователя
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_repeat": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Michael"
  }'
```

**Ответ (201):**
```json
{
  "status": "registered",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 2. Вход в систему
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

**Ответ (200):**
```json
{
  "token": "a1b2c3d4e5f6...",
  "expires_at": "2026-01-13T10:30:00Z",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 3. Обновление профиля
```bash
curl -X PUT http://localhost:8000/api/auth/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a1b2c3d4e5f6..." \
  -d '{
    "first_name": "Jane",
    "email": "jane@example.com"
  }'
```

**Ответ (200):**
```json
{
  "status": "updated",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "middle_name": "Michael"
  }
}
```

### 4. Выход из системы
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (204):** No Content

### 5. Удаление аккаунта
```bash
curl -X DELETE http://localhost:8000/api/auth/delete/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (204):** No Content

---

## Управление правами доступа (Admin API)

### 6. Назначить роль пользователю
```bash
curl -X POST http://localhost:8000/api/rbac/user-roles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin_token..." \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "role_name": "admin"
  }'
```

**Ответ (201):**
```json
{
  "status": "role assigned",
  "created": true
}
```

### 7. Удалить роль у пользователя
```bash
curl -X DELETE http://localhost:8000/api/rbac/user-roles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin_token..." \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "role_name": "user"
  }'
```

**Ответ (204):** No Content

### 8. Назначить права к роли
```bash
curl -X POST http://localhost:8000/api/rbac/permissions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin_token..." \
  -d '{
    "role_name": "user",
    "resource_code": "products",
    "action_code": "read"
  }'
```

**Ответ (201):**
```json
{
  "status": "permission assigned",
  "created": true
}
```

---

## Mock бизнес-ресурсы

### 9. Получить список продуктов
```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (200):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product 1",
      "price": 100
    },
    {
      "id": 2,
      "name": "Product 2",
      "price": 200
    }
  ]
}
```

### 10. Получить деталь продукта
```bash
curl -X GET http://localhost:8000/api/products/1/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (200):**
```json
{
  "id": 1,
  "name": "Product 1",
  "price": 100,
  "description": "Description 1"
}
```

### 11. Обновить продукт
```bash
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer a1b2c3d4e5f6..." \
  -d '{
    "name": "Updated Product",
    "price": 150
  }'
```

**Ответ (200):**
```json
{
  "status": "updated",
  "product": {
    "id": 1,
    "name": "Updated Product",
    "price": 150
  }
}
```

### 12. Удалить продукт
```bash
curl -X DELETE http://localhost:8000/api/products/1/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (204):** No Content

### 13. Получить список заказов
```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer a1b2c3d4e5f6..."
```

**Ответ (200):**
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

---

## Ошибки и их обработка

### 401 Unauthorized - нет аутентификации
```json
{
  "error": "Unauthorized"
}
```

### 403 Forbidden - нет прав доступа
```json
{
  "error": "Forbidden"
}
```

### 400 Bad Request - ошибка валидации
```json
{
  "error": "Field 'email' is required"
}
```
или
```json
{
  "error": "Passwords do not match"
}
```
или
```json
{
  "error": "User with this email already exists"
}
```

### 404 Not Found
```json
{
  "error": "User not found"
}
```

---

## Тестирование в Postman

### Шаг 1: Регистрация
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/register/`
- **Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123",
    "password_repeat": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### Шаг 2: Вход
- **Method**: POST
- **URL**: `http://localhost:8000/api/auth/login/`
- **Body** (JSON):
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123"
  }
  ```
- **Сохраните token из ответа**

### Шаг 3: Использование token для других запросов
- **Headers**:
  ```
  Authorization: Bearer {your_token_here}
  ```

### Шаг 4: Тестирование продуктов
- **Method**: GET
- **URL**: `http://localhost:8000/api/products/`
- **Headers**: 
  ```
  Authorization: Bearer {your_token}
  ```

---

## Сценарии тестирования доступа

### Сценарий 1: Admin имеет полный доступ
1. Создать пользователя с ролью `admin`
2. Admin может: читать, создавать, удалять продукты
3. Admin может управлять правами доступа

### Сценарий 2: User имеет ограниченный доступ
1. Создать пользователя с ролью `user`
2. User может: читать и создавать продукты
3. User НЕ может: удалять продукты
4. User НЕ может: управлять правами

### Сценарий 3: Guest имеет минимальный доступ
1. Создать пользователя с ролью `guest`
2. Guest может: только читать продукты
3. Guest НЕ может: создавать, редактировать, удалять
4. Guest НЕ может: управлять правами и заказами

---

## Python запросы (requests library)

```python
import requests

BASE_URL = "http://localhost:8000"

# Регистрация
response = requests.post(
    f"{BASE_URL}/api/auth/register/",
    json={
        "email": "user@example.com",
        "password": "SecurePass123",
        "password_repeat": "SecurePass123",
        "first_name": "John",
        "last_name": "Doe"
    }
)
print(response.json())

# Вход
response = requests.post(
    f"{BASE_URL}/api/auth/login/",
    json={
        "email": "user@example.com",
        "password": "SecurePass123"
    }
)
token = response.json()["token"]

# Получить продукты
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    f"{BASE_URL}/api/products/",
    headers=headers
)
print(response.json())
```

---

## JavaScript/Fetch запросы

```javascript
const BASE_URL = "http://localhost:8000";

// Вход
async function login() {
    const response = await fetch(`${BASE_URL}/api/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: 'user@example.com',
            password: 'SecurePass123'
        })
    });
    
    const data = await response.json();
    return data.token;
}

// Получить продукты
async function getProducts(token) {
    const response = await fetch(`${BASE_URL}/api/products/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}

// Использование
const token = await login();
const products = await getProducts(token);
console.log(products);
```

---

## Часто встречающиеся проблемы

### Проблема: 401 Unauthorized при попытке получить продукты
**Решение**: Убедитесь, что вы передали правильный token в заголовке Authorization

### Проблема: 403 Forbidden при попытке удалить продукт
**Решение**: Пользователь не имеет прав на action "delete" для resource "products"
- Назначьте пользователю роль "admin" или 
- Добавьте permission "products:delete" к его роли

### Проблема: 400 Bad Request при регистрации
**Решение**: Проверьте, что все обязательные поля заполнены и пароли совпадают

### Проблема: Token истек
**Решение**: Выполните новый login для получения свежего token
