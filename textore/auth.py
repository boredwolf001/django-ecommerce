from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

from shop.models import Cart

def register(request):
    if request.method == 'POST':
        errors = []
        if request.POST['name'] == '' or request.POST['password'] == '':
            errors.append('Please fill required fileds')
            return render(request, 'registration/register.html', {'errors': errors})
        if len(request.POST['password']) < 6:
            if 'Please fill required fileds' not in errors:
                errors.append('Password must be at least 6 charachters long')
            return render(request, 'registration/register.html', {'errors': errors})
        if request.POST['password'] != request.POST['confpassword']:
            if 'Please fill required fileds' not in errors:
                errors.append('Passwords didn\'t match')
            return render(request, 'registration/register.html', {'errors': errors})

        else:
            try:
                user = User.objects.create_user(
                    request.POST['name'], request.POST['email'], request.POST['password'])
                user.save()
                try:
                    cart = Cart.objects.create(user=user)
                    cart.save()
                except:
                    pass
                return HttpResponseRedirect('/auth/login')
            except IntegrityError:
                errors.append('User already exists')
                return render(request, 'registration/register.html', {'errors': errors})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        return render(request, 'registration/register.html')
