from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import Product

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart':cart})

def cart_add(request,id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))  # 'quantity' - name z inputa
        cart.add(product, qty)
    return redirect('product_details', id=id)

def cart_delete(request):

    pass

def cart_update(request):
    pass