import secrets
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User, AuthToken
from rbac.models import Role, UserRole


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Валидация обязательных полей
            required_fields = ['email', 'password', 'password_repeat', 'first_name', 'last_name']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {"error": f"Field '{field}' is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Проверка совпадения пароля
            if data["password"] != data["password_repeat"]:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверка длины пароля
            if len(data["password"]) < 8:
                return Response(
                    {"error": "Password must be at least 8 characters long"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создание пользователя
            user = User.objects.create(
                email=data["email"],
                password_hash=make_password(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_name=data.get("middle_name", ""),
            )
            
            # Назначение роли по умолчанию
            default_role = Role.objects.get(name="user")
            UserRole.objects.create(user=user, role=default_role)
            
            return Response(
                {
                    "status": "registered",
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                },
                status=status.HTTP_201_CREATED
            )
            
        except IntegrityError:
            return Response(
                {"error": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Role.DoesNotExist:
            return Response(
                {"error": "Default role 'user' not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            
            if not email or not password:
                return Response(
                    {"error": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.get(email=email, is_active=True)
            
            if not check_password(password, user.password_hash):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Создание токена
            token_value = secrets.token_hex(32)
            expires = now() + timedelta(hours=24)
            
            AuthToken.objects.create(
                user=user,
                token=token_value,
                expires_at=expires,
            )
            
            return Response(
                {
                    "token": token_value,
                    "expires_at": expires,
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request):
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        AuthToken.objects.filter(user=request.user).update(is_revoked=True)
        return Response(
            {"status": "logged out"},
            status=status.HTTP_204_NO_CONTENT
        )


class DeleteMeView(APIView):
    def delete(self, request):
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        request.user.is_active = False
        request.user.save()
        
        AuthToken.objects.filter(user=request.user).update(is_revoked=True)
        
        return Response(
            {"status": "account deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class UpdateUserView(APIView):
    def put(self, request):
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            data = request.data
            
            # Обновление доступных полей
            if "first_name" in data:
                request.user.first_name = data["first_name"]
            if "last_name" in data:
                request.user.last_name = data["last_name"]
            if "middle_name" in data:
                request.user.middle_name = data["middle_name"]
            
            # Обновление email (с проверкой уникальности)
            if "email" in data and data["email"] != request.user.email:
                if User.objects.filter(email=data["email"]).exists():
                    return Response(
                        {"error": "User with this email already exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                request.user.email = data["email"]
            
            request.user.save()
            
            return Response(
                {
                    "status": "updated",
                    "user": {
                        "id": str(request.user.id),
                        "email": request.user.email,
                        "first_name": request.user.first_name,
                        "last_name": request.user.last_name,
                        "middle_name": request.user.middle_name,
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )