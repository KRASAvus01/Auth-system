from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


def list_products_for_user(user):
    # Business logic placeholder: could filter by user permissions, tenant, etc.
    qs = Product.objects.all()
    return ProductSerializer(qs, many=True).data


def get_product_detail(product_id):
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None
    return ProductSerializer(p).data


def update_product(product_id, data):
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None
    serializer = ProductSerializer(p, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def delete_product(product_id):
    try:
        p = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return False
    p.delete()
    return True


def list_orders_for_user(user):
    qs = Order.objects.filter(user=user)
    return OrderSerializer(qs, many=True).data
