from django.contrib import admin
from rbac.models import Role, UserRole, Resource, Action, Permission, RolePermission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role__name')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code',)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('resource', 'action')
    search_fields = ('resource__code', 'action__code')


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    search_fields = ('role__name',)
