from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rbac.permissions import has_permission


class ProductListView(APIView):
    """Mock API для получения списка продуктов"""
    
    def get(self, request):
        """Получить список продуктов"""
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not has_permission(request.user, "products", "read"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mock данные
        products = [
            {"id": 1, "name": "Product 1", "price": 100},
            {"id": 2, "name": "Product 2", "price": 200},
            {"id": 3, "name": "Product 3", "price": 300},
        ]
        
        return Response({"products": products}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """Mock API для получения деталей продукта"""
    
    def get(self, request, product_id):
        """Получить детали продукта"""
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not has_permission(request.user, "products", "read"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mock данные
        products = {
            1: {"id": 1, "name": "Product 1", "price": 100, "description": "Description 1"},
            2: {"id": 2, "name": "Product 2", "price": 200, "description": "Description 2"},
            3: {"id": 3, "name": "Product 3", "price": 300, "description": "Description 3"},
        }
        
        product = products.get(product_id)
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(product, status=status.HTTP_200_OK)
    
    def put(self, request, product_id):
        """Обновить продукт"""
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not has_permission(request.user, "products", "write"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mock: просто возвращаем обновленные данные
        updated_product = {
            "id": product_id,
            **request.data
        }
        
        return Response(
            {"status": "updated", "product": updated_product},
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, product_id):
        """Удалить продукт"""
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not has_permission(request.user, "products", "delete"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
            {"status": "deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class OrderListView(APIView):
    """Mock API для получения списка заказов"""
    
    def get(self, request):
        """Получить список заказов"""
        if not request.user:
            return Response(
                {"error": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not has_permission(request.user, "orders", "read"):
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mock данные
        orders = [
            {"id": 1, "user_id": str(request.user.id), "product_id": 1, "quantity": 2},
            {"id": 2, "user_id": str(request.user.id), "product_id": 2, "quantity": 1},
        ]
        
        return Response({"orders": orders}, status=status.HTTP_200_OK)
