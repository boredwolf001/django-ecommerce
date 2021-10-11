from django.urls import path

from .views import index, shop, product, cart, updateCart, addToCart, deleteFromCart, add_new_product, edit_product, checkout

app_name = 'shop'
urlpatterns = [
    path('', index, name='shop'),
    path('cart/', cart, name='cart'),
    path('addtocart/<slug>', addToCart, name='addtocart'),
    path('cart/update/<id>', updateCart, name='updatecart'),
    path('cart/delete/<id>', deleteFromCart, name='deletecart'),
    path('shop/', shop, name='index'),
    path('products/<slug>', product, name='singleproduct'),
    path('addproduct/', add_new_product, name='addproduct'),
    path('editproduct/<slug>', edit_product, name='editproduct'),
    path('checkout/', checkout, name='checkout'),
]