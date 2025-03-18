from rest_framework import serializers
from .models import Typ, Menu, Table, Order, OrderItem, DeliveryOrder, DeliveryItem, ServerOrder
from django.contrib.auth.models import User

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ✅ Typ Serializer
class TypSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typ
        fields = '__all__'

# ✅ Menu Serializer
class MenuSerializer(serializers.ModelSerializer):
    typ = TypSerializer()  # Nested Typ Serializer

    class Meta:
        model = Menu
        fields = '__all__'

# ✅ Table Serializer
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

# ✅ OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuSerializer()  # Nested Menu Serializer

    class Meta:
        model = OrderItem
        fields = '__all__'

# ✅ Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested User Serializer
    table = TableSerializer()  # Nested Table Serializer
    items = OrderItemSerializer(many=True)  # Nested Items

    class Meta:
        model = Order
        fields = '__all__'

# ✅ DeliveryItem Serializer
class DeliveryItemSerializer(serializers.ModelSerializer):
    menu_item = MenuSerializer()  # Nested Menu Serializer

    class Meta:
        model = DeliveryItem
        fields = '__all__'

# ✅ DeliveryOrder Serializer
class DeliveryOrderSerializer(serializers.ModelSerializer):
    items = DeliveryItemSerializer(many=True)  # Nested Items

    class Meta:
        model = DeliveryOrder
        fields = '__all__'

# ✅ ServerOrder Serializer
class ServerOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested User Serializer

    class Meta:
        model = ServerOrder
        fields = '__all__'
