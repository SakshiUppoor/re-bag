from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from .forms import *
import datetime
from django.utils import timezone
from .models import *
# Create your views here.

User = get_user_model()

@login_required(login_url='/login/')
def createProduct(request):
    if request.method == 'POST':
        i = ItemForm(request.POST)
        print(i.errors)
        item = i.save()
        item.seller = request.user
        print(item)
        item.save()
        a = AuctionForm(request.POST)
        print(a.errors)
        auction = a.save(commit=False)
        auction.item = item
        auction.save()
    form1 = ItemForm()
    form2 = AuctionForm()

    context = {
        'form1': form1,
        'form2': form2,
    }

    return render(request, 'productForm.html', context)


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
def categoryShop(request, url_category):
    categories= Category.objects.all()
    current= timezone.now() 
    print(url_category)
    if url_category == "All Products":
        items= Item.objects.all()
    else:
        items= Item.objects.filter(cat=url_category)
    item_ids = items.values_list('id', flat=True)
    relevant_auctions = Auction.objects.filter(item_id__in = item_ids, cap__gte = current)
    ongoing= relevant_auctions.filter(start__lte = current)
    upcoming = relevant_auctions.filter(start__gte = current)

    
    # auctions= Auction.objects.all()
    # ongoing={}
    # upcoming={}
    # j=0
    # k=0
    # for i in auctions:
    #     print(url_category,i.item.cat.category,i.item.cat.category==url_category)
    #     if url_category =="All Products":
    #         if i.start < current and i.cap > current:
    #             ongoing[j]=i
    #             j=j+1
    #         elif i.start > current:
    #             upcoming[k]=i
    #             k=k+1
    #     elif i.item.cat.category == url_category and url_category != "All Products":
    #         if i.start < current and i.cap > current:
    #             ongoing[j]=i
    #             j=j+1
    #         elif i.start > current:
    #             upcoming[k]=i
    #             k=k+1   
    #     else:
    #         print('noooooo') 
    print(ongoing,upcoming)    
    return render(request, "categoryShop.html", {'categories': categories, 'url_category': url_category,'upcoming':upcoming, 'ongoing':ongoing})


def shop(request):
    categories= Category.objects.all()
    auction_items = Auction.objects.all()
    ongoing = {}
    upcoming = {}
    j=0
    k=0
    current= timezone.now() 
    for i in auction_items:
        if i.start < current and i.cap > current:
            ongoing[j]=i
            j=j+1
        elif i.start > current:
            upcoming[k]=i
            k=k+1
    print(current)
    print(upcoming, ongoing)
    return render(request, "product.html", {'categories': categories, 'auction':auction_items, 'ongoing':ongoing, 'upcoming':upcoming, "current":current})
