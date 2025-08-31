from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart , name='cart'),
    path('cart-delete/<int:id>', cart_delete, name='cart_delete'),
    path('cart-add/<int:id>/', cart_add, name='cart_add'),
    # path('cart-update', cart_update, name='cart_update'),
    path('cart-payment/',cart_payment, name='cart_payment'),
    path('checkout/', checkout, name='checkout'),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook")
]