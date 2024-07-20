from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to="product", null=True)
    description = models.TextField(blank=True, null=True)
    availability = models.BooleanField()
    price = models.FloatField(blank=False, null=False)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False) 
    email = models.EmailField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=False, null=False)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return  f"{self.quantity} x  {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    product = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.name