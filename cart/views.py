from django.utils import timezone

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
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )

            request.session["current_order_id"] = order.id
            return redirect('cart_payment')
    else:
        form = order_form()
    return render(request, 'checkout.html', {'form': form, 'cart': cart})

def cart_payment(request):
    order_id = request.session.get("current_order_id")
    if order_id:
        order = get_object_or_404(Order, id=order_id, customer=request.user)
    else:
        order = Order.objects.filter(customer=request.user, status=Order.Status.PENDING)\
                             .order_by("-created").first()
        if not order:
            return redirect("cart")

    Order.objects.filter(customer=request.user,
                         status=Order.Status.PENDING
                         ).exclude(id=order.id).delete()

    if request.method == 'POST':
        line_items = []
        for item in order.items.all():
            line_items.append({
                "price_data": {
                    "currency": "pln",
                    "product_data": {"name": item.product.name},
                    "unit_amount": int(item.product.price * 100),
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

        Payment.objects.update_or_create(
            order=order,
            defaults={"stripe_checkout_id": session.id,
                      "status": Payment.PaymentStatus.PENDING}
        )

        return redirect(session.url, code=303)

    return render(request, 'cart_payment.html', {"order": order})

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


def payment_success(request):
    cart = Cart(request)
    cart.clear()
    request.session.pop("current_order_id", None)
    return render(request, "payment_success.html")


def payment_cancel(request):
    return render(request, "payment_cancel.html")