from rbac.models import RolePermission


def has_permission(user, resource_code, action_code) -> bool:
    return RolePermission.objects.filter(
        role__userrole__user=user,
        permission__resource__code=resource_code,
        permission__action__code=action_code,
    ).exists()