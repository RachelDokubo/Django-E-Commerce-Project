from django.contrib import admin
from .models import Product, Contact, CartItem, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(Order)