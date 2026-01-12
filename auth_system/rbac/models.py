import uuid
from django.db import models
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)


class UserRole(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'role')


class Resource(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)


class Action(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)


class Permission(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('resource', 'action')


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('role', 'permission')