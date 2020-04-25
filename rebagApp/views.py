from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from .forms import *

# Create your views here.

User = get_user_model()


def createProduct(request):
    if request.method == 'POST':
        i = ItemForm(request.POST)
        i.save()
        a = AuctionForm(request.POST)
        a.save()
    else:
        form1 = ItemForm()
        form2 = AuctionForm()

        context = {
            'form1': form1,
            'form2': form2,
        }

    return render(request, 'add_product.html', context)


def room(request, room_name):
    auction = Auction.objects.get(id=room_name)
    item = auction.item
    cart = Item.objects.filter(buyer=request.user)
    d = auction.cap_time
    print(d.strftime('%H:%M'))
    return render(request, 'auction.html', {
        'auction': auction,
        'room_name': room_name,
        'user': request.user,
        'item': item,
        'deadline': auction.cap_time,
        'cart': cart,
    })


def home(request):
    return render(request, "base.html")


def register(request):

    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return HttpResponseRedirect(reverse('register'))
            else:
                user = User.objects.create_user(
                    first_name=f_name, last_name=l_name, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect(reverse('home'))
        else:
            messages.info(request, 'Password not matching')
            return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'signup.html', {'page': 'signup'})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or password incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html', {'page': 'login'})


def user_logout(request):
    auth.logout(request)
    return redirect(reverse('login'))
