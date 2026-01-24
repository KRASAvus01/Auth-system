from django.contrib import admin
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, DeleteMeView, UpdateUserView
from rbac.views import RolePermissionView, UserRoleView
from mock_resources.views import ProductListView, ProductDetailView, OrderListView

# Swagger / OpenAPI
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Auth System API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/delete/', DeleteMeView.as_view(), name='delete_user'),
    path('api/auth/update/', UpdateUserView.as_view(), name='update_user'),
    
    # RBAC endpoints (Admin API)
    path('api/rbac/permissions/', RolePermissionView.as_view(), name='role_permissions'),
    path('api/rbac/user-roles/', UserRoleView.as_view(), name='user_roles'),
    
    # Mock business resources
    path('api/products/', ProductListView.as_view(), name='product_list'),
    path('api/products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/orders/', OrderListView.as_view(), name='order_list'),
    # Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
