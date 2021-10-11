from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .forms import ProductForm
from .models import Product, Cart, CartItem

def index(request):
    products = Product.objects.all().order_by('title')[:20]

    return render(request, 'pages/home.html', {'products': products})

def shop(request):
    products = Product.objects.all().order_by('title')

    return render(request, 'pages/shop.html' , {'products': products})

def product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'pages/product.html', {'product': product})

def cart(request):
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    user = User.objects.get(username=request.user.username)
    cart = user.cart
    cart_items = cart.cartitem_set.all()

    print(cart_items)

    return render(request, 'pages/cart.html', {'cart_items': cart_items, 'user': user})

@csrf_exempt
def updateCart(request, id):
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        new_qty = int(request.POST.get('qty', 0.0))
        cartItem = CartItem.objects.get(pk=id)

        cartItem.quantity = new_qty
        cartItem.set_price()
        cartItem.save()

        return HttpResponseRedirect('/cart')

def addToCart(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    user = User.objects.get(username=request.user.username)
    cart = Cart.objects.get(user=user)
    product = Product.objects.get(slug=slug)
    cartitem = user.cart.cartitem_set.create(product=product, cart=cart)
    cartitem.set_price()
    cartitem.save()

    return HttpResponseRedirect('/shop')

def deleteFromCart(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    cartitem = CartItem.objects.get(pk=id)
    if cartitem.cart.user.username != request.user.username:
        return HttpResponseRedirect('/cart')
    cartitem.delete()
    return HttpResponseRedirect('/cart')

def add_new_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        new_product = product_form.save()
        new_product.set_slug()
        new_product.save()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            form = ProductForm()
            return render(request, 'pages/newproduct.html', {'form': form})
        else:
            return HttpResponseRedirect('/shop')
    else:
        return HttpResponseRedirect('/login')

def edit_product(request, slug):
    if request.method == 'POST':
        product = Product.objects.get(slug=slug)
        f = ProductForm(request.POST, request.FILES, instance=product)
        updated_prodcut = f.save()
        updated_prodcut.save()

    product = Product.objects.get(slug=slug)
    form = ProductForm(instance=product)
    return render(request, 'pages/editproduct.html', {'form': form})

def checkout(request):
    return render(request, 'pages/checkout.html')