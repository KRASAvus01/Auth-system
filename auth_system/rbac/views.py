from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rbac.permissions import has_permission
from rbac.models import Role, Resource, Action, Permission, RolePermission, UserRole
from users.models import User


class RolePermissionView(APIView):
    """Admin API для управления правами доступа"""
    
    def post(self, request):
        """Добавить права к роли"""
        if not request.user or not has_permission(request.user, "rbac", "assign_role"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            role_name = request.data.get("role_name")
            resource_code = request.data.get("resource_code")
            action_code = request.data.get("action_code")

            if not all([role_name, resource_code, action_code]):
                return Response(
                    {"error": "role_name, resource_code, and action_code are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            role = Role.objects.get(name=role_name)
            resource = Resource.objects.get(code=resource_code)
            action = Action.objects.get(code=action_code)

            permission, _ = Permission.objects.get_or_create(
                resource=resource,
                action=action
            )

            role_permission, created = RolePermission.objects.get_or_create(
                role=role,
                permission=permission
            )

            return Response(
                {
                    "status": "permission assigned",
                    "created": created
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except Role.DoesNotExist:
            return Response(
                {"error": "Role not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except (Resource.DoesNotExist, Action.DoesNotExist):
            return Response(
                {"error": "Resource or Action not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRoleView(APIView):
    """Admin API для назначения ролей пользователям"""
    
    def post(self, request):
        """Назначить роль пользователю"""
        if not request.user or not has_permission(request.user, "rbac", "assign_role"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user_id = request.data.get("user_id")
            role_name = request.data.get("role_name")

            if not user_id or not role_name:
                return Response(
                    {"error": "user_id and role_name are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id=user_id)
            role = Role.objects.get(name=role_name)

            user_role, created = UserRole.objects.get_or_create(
                user=user,
                role=role
            )

            return Response(
                {
                    "status": "role assigned",
                    "created": created
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Role.DoesNotExist:
            return Response(
                {"error": "Role not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request):
        """Удалить роль у пользователя"""
        if not request.user or not has_permission(request.user, "rbac", "assign_role"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user_id = request.data.get("user_id")
            role_name = request.data.get("role_name")

            if not user_id or not role_name:
                return Response(
                    {"error": "user_id and role_name are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id=user_id)
            role = Role.objects.get(name=role_name)

            UserRole.objects.filter(user=user, role=role).delete()

            return Response(
                {"status": "role removed"},
                status=status.HTTP_204_NO_CONTENT
            )

        except (User.DoesNotExist, Role.DoesNotExist):
            return Response(
                {"error": "User or Role not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )