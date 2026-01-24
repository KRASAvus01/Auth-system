from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rbac.permissions import has_permission

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from . import services


class ProductListView(APIView):
    """API для получения списка продуктов (использует ORM и сериализаторы)"""

    def get(self, request):
        if not getattr(request.user, 'is_authenticated', False):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "products", "read"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        products = services.list_products_for_user(request.user)
        return Response({"products": products}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """API для деталей/изменения/удаления продукта"""

    def get(self, request, product_id):
        if not getattr(request.user, 'is_authenticated', False):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "products", "read"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        product = services.get_product_detail(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(product, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        if not getattr(request.user, 'is_authenticated', False):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "products", "write"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        updated = services.update_product(product_id, request.data)
        if not updated:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "updated", "product": updated}, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        if not getattr(request.user, 'is_authenticated', False):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "products", "delete"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        ok = services.delete_product(product_id)
        if not ok:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "deleted"}, status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    """API для получения заказов пользователя"""

    def get(self, request):
        if not getattr(request.user, 'is_authenticated', False):
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "orders", "read"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        orders = services.list_orders_for_user(request.user)
        return Response({"orders": orders}, status=status.HTTP_200_OK)
