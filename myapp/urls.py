# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),
    path('types/', TypListCreateAPIView.as_view(), name='typ-list'),
    path('types/<int:pk>/', TypRetrieveUpdateDestroyAPIView.as_view(), name='typ-detail'),

    path('menus/', MenuListCreateAPIView.as_view(), name='menu-list'),
    path('menus/<int:pk>/', MenuRetrieveUpdateDestroyAPIView.as_view(), name='menu-detail'),

    path('tables/', TableListCreateAPIView.as_view(), name='table-list'),
    path('tables/<int:pk>/', TableRetrieveUpdateDestroyAPIView.as_view(), name='table-detail'),

    path('orders/', OrderListCreateAPIView.as_view(), name='order-list'),
    path('orders/create/', OrderAPIView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),

    path('order-items/', OrderItemListCreateAPIView.as_view(), name='order-item-list'),
    path('order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='order-item-detail'),

    path('delivery-orders/', DeliveryOrderListCreateAPIView.as_view(), name='delivery-order-list'),
    path('delivery-orders/<int:pk>/', DeliveryOrderRetrieveUpdateDestroyAPIView.as_view(), name='delivery-order-detail'),

    path('server-orders/', ServerOrderListCreateAPIView.as_view(), name='server-order-list'),
    path('server-orders/<int:pk>/', ServerOrderRetrieveUpdateDestroyAPIView.as_view(), name='server-order-detail'),

    path('orders/new/', NewOrdersAPIView.as_view(), name='new-orders'),
    path('orders/print/', MarkOrderPrintedAPIView.as_view(), name='mark-order-printed'),
    path('delivery-orders/print/', MarkDeliveryOrderPrintedAPIView.as_view(), name='mark-delivery-order-printed'),

    path('orders/submit/', SubmitOrderAPIView.as_view(), name='submit-order'),
    path('delivery-orders/submit/', DeliverySubmitOrderAPIView.as_view(), name='submit-delivery-order'),

    # ✅ Confirm Order
    path('orders/confirm/', UpdateOrderStatusAPIView.as_view(), name='confirm-order'),

    # ✅ Cancel Order
    path('orders/cancel/', UpdateOrderStatusAPIView.as_view(), name='cancel-order'),

    # ✅ Confirm Delivery Order
    path('delivery-orders/confirm/', UpdateOrderStatusAPIView.as_view(), name='confirm-delivery'),

    # ✅ Cancel Delivery Order
    path('delivery-orders/cancel/', UpdateOrderStatusAPIView.as_view(), name='cancel-delivery'),
]
