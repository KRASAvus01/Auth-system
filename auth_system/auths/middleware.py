from django.utils.timezone import now
from django.http import JsonResponse
from users.models import AuthToken


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token_value = auth_header.split(" ")[1]

            try:
                token = AuthToken.objects.select_related("user").get(
                    token=token_value,
                    is_revoked=False,
                    expires_at__gt=now(),
                    user__is_active=True,
                )
                request.user = token.user
            except AuthToken.DoesNotExist:
                pass

        return self.get_response(request)