from django.forms import ModelForm

from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'short_description', 'long_description', 'in_stock', 'price', 'product_image')