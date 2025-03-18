from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
from rest_framework import generics , permissions
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db import transaction
import json
import logging

# ✅ User Login API View
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow anyone to access

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Log in user
            token, created = Token.objects.get_or_create(user=user)  # Get or create a token
            
            return Response({
                'message': 'Logged in successfully.',
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ User Logout API View
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

    def post(self, request):
        request.user.auth_token.delete()  # Delete the token
        logout(request)  # Log out the user
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Check if both passwords are provided
        if not current_password or not new_password:
            return Response({'error': 'Both current and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if current password is correct
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password strength
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Change the password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
# ✅ Typ API
class TypListCreateAPIView(generics.ListCreateAPIView):
    queryset = Typ.objects.all()
    serializer_class = TypSerializer
    permission_classes = [permissions.AllowAny]

class TypRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Typ.objects.all()
    serializer_class = TypSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Menu API
class MenuListCreateAPIView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]

class MenuRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Table API
class TableListCreateAPIView(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]

class TableRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]

# ✅ Order API
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.filter(status='pending')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ OrderItem API
class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Delivery Order API
class DeliveryOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = DeliveryOrder.objects.all()
    serializer_class = DeliveryOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryOrder.objects.all()
    serializer_class = DeliveryOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Delivery Item API
class DeliveryItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = DeliveryItem.objects.all()
    serializer_class = DeliveryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeliveryItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryItem.objects.all()
    serializer_class = DeliveryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Server Order API
class ServerOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServerOrder.objects.all()
    serializer_class = ServerOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServerOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServerOrder.objects.all()
    serializer_class = ServerOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Utility Function to Format Orders
def format_order(order, is_delivery=False):
    """Format order details for response."""
    order_details = []
    for item in order.items.all():
        order_details.append(f"({item.quantity}) {item.menu_item} ({item.comment})")

    formatted_order = "\n".join(order_details)

    if is_delivery:
        customer_info = f"New delivery order for {order.customer_phone}"
    else:
        customer_info = f"New order for {order.table}"

    return [order.id, f"{customer_info}:\nItems:\n{formatted_order}\n", f"{order.total_price:.2f}"]

# ✅ Fetch Unprinted Orders
class NewOrdersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = []

        # Fetch unprinted regular orders
        orders = Order.objects.filter(is_printed=False)
        for order in orders:
            messages.append(format_order(order))
            order.is_printed = True
            order.save()

        # Fetch unprinted delivery orders
        delivery_orders = DeliveryOrder.objects.filter(is_printed=False)
        for order in delivery_orders:
            messages.append(format_order(order, is_delivery=True))
            order.is_printed = True
            order.save()

        return Response({"messages": messages}, status=status.HTTP_200_OK)

# ✅ Mark an Order as Printed
class MarkOrderPrintedAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.is_printed = True
            order.save()
            return Response({"message": "Order marked as printed."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

# ✅ Mark a Delivery Order as Printed
class MarkDeliveryOrderPrintedAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        try:
            order = DeliveryOrder.objects.get(id=order_id)
            order.is_printed = True
            order.save()
            return Response({"message": "Delivery order marked as printed."}, status=status.HTTP_200_OK)
        except DeliveryOrder.DoesNotExist:
            return Response({"error": "Delivery order not found."}, status=status.HTTP_404_NOT_FOUND)
        

logger = logging.getLogger(__name__)

# ✅ Submit Order (For Dine-in Tables)
class SubmitOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure authenticated user

    @transaction.atomic  # Ensures atomic transactions
    def post(self, request):
        try:
            # Parse JSON data
            data = request.data
            table_number = data.get('table_number')
            items = data.get('items', [])
            total_price = float(data.get('total_price', 0))

            # Validate required fields
            if not table_number or not items or total_price <= 0:
                return Response({"error": "Invalid or missing data"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch table and create order
            table = get_object_or_404(Table, number=table_number)
            order = Order.objects.create(table=table, total_price=total_price, user=request.user)

            # Add order items
            order_details, item_count = [], 0
            for item in items:
                menu_item = get_object_or_404(Menu, id=item['id'])
                quantity = int(item.get('quantity', 1))
                comment = item.get('comment', '')

                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, comment=comment)
                order_details.append(f"{quantity} x {menu_item.name} ({comment})" if comment else f"{quantity} x {menu_item.name}")
                item_count += quantity

            # Update Server Order count
            server_order, created = ServerOrder.objects.get_or_create(user=request.user, defaults={'order': 0})
            server_order.order = F('order') + item_count
            server_order.save()

            # WebSocket Notification (Optional)
            formatted_order = "\n".join(order_details)
            message = f"New order for Table {table_number}:\nItems:\n{formatted_order}\nTotal Price: {total_price:.2f} DZD"

            return Response({"message": "Order submitted successfully!"}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Table.DoesNotExist:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)
        except Menu.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error submitting order: {e}")
            return Response({"error": f"Error submitting order: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Submit Delivery Order (For Delivery)
class DeliverySubmitOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure authenticated user

    @transaction.atomic
    def post(self, request):
        try:
            # Parse JSON data
            data = request.data
            customer_phone = data.get('customer_phone')
            items = data.get('items', [])
            total_price = float(data.get('total_price', 0))

            if not customer_phone or not items or total_price <= 0:
                return Response({"error": "Invalid or missing data"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new delivery order
            order = DeliveryOrder.objects.create(customer_phone=customer_phone, total_price=total_price)

            order_details = []
            for item in items:
                menu_item = get_object_or_404(Menu, id=item['id'])
                quantity = int(item.get('quantity', 1))
                comment = item.get('comment', '')

                DeliveryItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, comment=comment)
                order_details.append(f"{quantity} x {menu_item.name} ({comment})" if comment else f"{quantity} x {menu_item.name}")

            # WebSocket Notification (Optional)
            formatted_order = "\n".join(order_details)
            message = f"New delivery order for {customer_phone}:\nItems:\n{formatted_order}\nTotal Price: {total_price:.2f} DZD"


            return Response({"message": "Delivery order submitted successfully!"}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Menu.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error submitting delivery order: {e}")
            return Response({"error": "An internal error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateOrderStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        order_type = request.data.get('order_type')
        status_update = request.data.get('status')

        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Determine if the order is a regular Order or a DeliveryOrder
        if order_type == 'order':
            model = Order
        elif order_type == 'delivery':
            model = DeliveryOrder
        else:
            return Response({'error': 'Invalid order type'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the order
        order = get_object_or_404(model, id=order_id)

        # Update status based on action
        if status_update == 'complete':
            order.status = 'completed'
        elif status_update == 'cancel':
            order.status = 'canceled'
        else:
            return Response({'error': 'Invalid status update'}, status=status.HTTP_400_BAD_REQUEST)

        order.save()

        return Response({'message': f"Order marked as {order.status}."}, status=status.HTTP_200_OK)
    

class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        table_id = data.get('table_id')
        items = data.get('items', [])

        if not items:
            return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        table = None
        if table_id:
            try:
                table = Table.objects.get(id=table_id)
            except Table.DoesNotExist:
                return Response({"error": "Table not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(user=user, table=table)
        total_price = 0
        
        for item in items:
            try:
                menu_item = Menu.objects.get(id=item['menu_id'])
                quantity = item.get('quantity', 1)
                comment = item.get('comment', '')
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, comment=comment)
                total_price += menu_item.price * quantity
            except Menu.DoesNotExist:
                return Response({"error": f"Menu item with ID {item['menu_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)

        order.total_price = total_price
        order.save()

        return Response({"message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)