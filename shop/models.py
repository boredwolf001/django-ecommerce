from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from slugify import slugify

class Product(models.Model):
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    slug = models.CharField(null=True, blank=True, max_length=200)
    in_stock = models.BooleanField(default=True)
    price = models.FloatField()
    product_image = models.ImageField(default='default-product-image.png', upload_to='product_images')

    def set_slug(self):
        self.slug = slugify(self.title)

    def __str__(self):
        return self.title
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def set_price(self):
        self.price = self.product.price * self.quantity

    
    def __str__(self):
        return f"{self.product.title}'s cart item"

