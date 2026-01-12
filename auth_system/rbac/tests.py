from django.test import TestCase
from rbac.models import Role, Resource, Action, Permission


class RBACModelTests(TestCase):
    def test_permission_creation(self):
        role = Role.objects.create(name="tester")
        resource = Resource.objects.create(code="reports")
        action = Action.objects.create(code="read")

        permission = Permission.objects.create(
            resource=resource,
            action=action
        )

        self.assertEqual(permission.resource.code, "reports")
        self.assertEqual(permission.action.code, "read")