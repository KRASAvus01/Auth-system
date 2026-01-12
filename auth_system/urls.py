from django.contrib import admin
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, DeleteMeView, UpdateUserView
from rbac.views import RolePermissionView, UserRoleView
from mock_resources.views import ProductListView, ProductDetailView, OrderListView


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
]
