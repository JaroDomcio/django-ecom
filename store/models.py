from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.name



class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'pending'
        IN_PROGRESS = 'IN_PROGRESS', 'in_progress'
        COMPLETED = 'COMPLETED', 'completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    customer = models.ForeignKey(User, on_delete = models.PROTECT)

    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=50,choices=Status.choices, default=Status.PENDING)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer}'s Order"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete = models.PROTECT)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name