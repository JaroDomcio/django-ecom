from django.db import models

from store.models import Order


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "pending"
        PAID = "PAID", "paid"
        FAILED = "FAILED", "failed"
        CANCELED = "CANCELED", "canceled"

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")

    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_checkout_id = models.CharField(max_length=100, unique=True)
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    has_paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Payment #{self.pk} for Order #{self.order_id} • {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["stripe_checkout_id"]),
            models.Index(fields=["stripe_payment_intent_id"]),
        ]


