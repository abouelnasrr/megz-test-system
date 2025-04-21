from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class ProductColor(models.Model):
    product_id = models.IntegerField()
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Product {self.product_id} - {self.color} - {self.quantity} items"


# Create your models here.
class Products(models.Model):
 
    def __str__(self):
        return self.title
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    stock = models.IntegerField(default=0)  # New field for stock

 
 
class Order(models.Model):
 
    
    items = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    email =models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    total = models.CharField(max_length=200)
    
class History(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    id_number = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # ✅ Added field for notes
    items = models.TextField()  # Store items as a serialized string
    total = models.FloatField()
    colors = models.TextField(blank=True, null=True)  # ✅ Save colors here
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"History {self.id} - {self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

class SpareEntry(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    action = models.CharField(max_length=10, choices=[("returned", "Returned"), ("destroyed", "Destroyed")])
    timestamp = models.DateTimeField(default=now)  # Store date/time of action

    def __str__(self):
        return f"{self.product.title} - {self.quantity} {self.action} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)  # Store hashed passwords
    created_at = models.DateTimeField(auto_now_add=True)
    # plain_password = models.CharField(max_length=128, blank=True, null=True)  # Store the original password

    def __str__(self):
        return self.username


class Users(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # DO NOT HASH (Not recommended)

from django.db import models

class WebsiteLogo(models.Model):
    image = models.ImageField(upload_to='logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Logo uploaded on {self.uploaded_at}"
