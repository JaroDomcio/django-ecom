from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart
from store.models import Product, Order, OrderItem
from cart.models import Payment
from .forms import order_form

from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    order = get_object_or_404(Order, customer=request.user, status=Order.Status.PENDING)

    if request.method == 'POST':
        line_items = []
        for item in order.items.all():
            line_items.append({
                "price_data":{
                    "currency":"pln",
                    "product_data": {"name":item.product.name},
                    "unit_amount": int(item.product.price*100),
                },
                "quantity": item.quantity,
            })
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=request.build_absolute_uri(reverse("payment_success")),
            cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
            customer_email=request.user.email,
        )

        # Utwórz obiekt Payment
        Payment.objects.create(
            order=order,
            stripe_checkout_id=session.id,
            status=Payment.PaymentStatus.PENDING
        )

    return render(request, 'cart_payment.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        checkout_id = session["id"]

        try:
            payment = Payment.objects.select_related("order").get(stripe_checkout_id=checkout_id)
        except Payment.DoesNotExist:
            return HttpResponse(status=200)

        payment.status = Payment.PaymentStatus.PAID
        payment.has_paid = True
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "has_paid", "paid_at"])

        order = payment.order
        order.status = Order.Status.COMPLETED
        order.save(update_fields=["status"])

    return HttpResponse(status=200)
