from django.db import models

class Category(models.Model):
    name = models.CharField(max_lenght=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_lenght=50)
    last_name = models.CharField(max_lenght=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'pending'
        COMPLETED = 'COMPLETED', 'completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField()
    phone = models.CharField(max_length=10)
    status = models.CharField(choices=Status.choices)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name