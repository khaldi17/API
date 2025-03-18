# myapp/admin.py
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Typ)
admin.site.register(Menu)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryOrder)
admin.site.register(DeliveryItem)



