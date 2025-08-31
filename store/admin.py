from django.contrib import admin

from cart.models import Payment
from .models import Category, Product, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Payment)