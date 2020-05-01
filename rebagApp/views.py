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

@login_required(login_url='/login/')
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


# def home(request):
#     form1 = ProductForm()
#     form2 = AuctionForm()
#     return render(request, "base.html",{'form1': form1, 'form2': form2})


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
        items= Item.objects.filter(category__category=url_category)
    item_ids = items.values_list('id', flat=True)
    relevant_auctions = Auction.objects.filter(item_id__in = item_ids, cap_time__gte = current)
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
    items = list(Item.objects.all())
    print(items)
    live_items = []
    upcoming_items = []
    for item in items:
        if item.auction_status == "live":
            live_items.append(item)
        elif item.auction_status == "upcoming":
            upcoming_items.append(item)
    live_items.sort(key=Item.time_to_end, reverse=True)
    print(live_items)
    print(items)
    """
    auction_items = Auction.objects.all()
    ongoing = {}
    upcoming = {}
    j=0
    k=0
    current= timezone.now() 
    for i in auction_items:
        if i.start < current and i.cap_time > current:
            ongoing[j]=i
            j=j+1
        elif i.start > current:
            upcoming[k]=i
            k=k+1
    print(current)
    print(upcoming, ongoing)
    return render(request, "product.html", {'categories': categories, 'auction':auction_items, 'ongoing':ongoing, 'upcoming':upcoming, "current":current})
    """
    return render(request, "product.html", {'categories': categories,'items':items})

def addProduct(request):
    if request.method == 'POST':
        d1 = {key:request.POST[key] for key in ["item_name", "item_description", "condition", "base_price", "cat"]}
        d2 = {key:request.POST[key] for key in ["start", "cap"]}
        print(d1)
        print(d2)
        form1 = ItemForm(d1)
        form2 = AuctionForm(d2)
        print(form1.is_valid())
        print(form2.is_valid())
        if form1.is_valid() and form2.is_valid():
            f1=form1.save(commit=False)
            f1.seller = request.user
            f1.save()
            f2=form2.save(commit=False)
            f2.item = f1.id
            f2.save()
    else:
        form1 = ItemForm()
        form2 = AuctionForm()
    return render(request, 'home.html', {'form1': form1, 'form2': form2})

def home(request):
    print("helloooooooooooooooooooooooooooooooooo")
    items = Item.objects.all()
    feature1 = items[0]
    feature2 = items[1]
    feature3 = items[2]
    categories = Category.objects.all()
    print("!!!!!!!!!!!!!!!!!",feature3.item_images.first().image.url)
    context = {
        'first':feature1,
        'second':feature2,
        'third':feature3,
        'items':items,
        'categories':categories,
    }
    return render(request, 'home.html', context)