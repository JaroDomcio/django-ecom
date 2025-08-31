from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import Product, Order, OrderItem
from .forms import order_form

def cart(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart':cart})

def cart_add(request,id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))
        cart.add(product, qty)
    return redirect('product_details', id=id)

def cart_delete(request,id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart')

def cart_update(request):
    pass


def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        form = order_form(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer=request.user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                phone=form.cleaned_data['phone'],
                status=Order.Status.PENDING
            )
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'])
            return redirect('cart_payment')
    else:
        form = order_form()
    return render(request, 'checkout.html', {'form':form, 'cart':cart})


def cart_payment(request):
    return render(request, 'cart_payment.html')