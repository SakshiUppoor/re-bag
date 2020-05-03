from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from datetime import timedelta
from .forms import *
import datetime
from django.utils import timezone
from .models import *
# Create your views here.

User = get_user_model()

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

def home(request):
    items = Item.objects.all()
    print(items)
    feature1 = items[0]
    feature2 = items[1]
    feature3 = items[2]
    categories = Category.objects.all()
    context = {
        'first':feature1,
        'second':feature2,
        'third':feature3,
        'items':items,
        'categories':categories,
        'cart': Item.objects.filter(buyer=request.user),
    }
    return render(request, 'home.html', context)

    
@login_required(login_url='/login/')
def createProduct(request):
    if request.method == 'POST':
        i = ItemForm(request.POST)
        print(i.errors)
        item = i.save()
        item.seller = request.user
        item.current_price = item.base_price
        image = request.FILES['image']
        if image:
            new_image = Image(image=image, item=item)
            new_image.save()
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

def detail(request, slug):
    context = {
        'item':Item.objects.get(slug=slug),
        'cart': Item.objects.filter(buyer=request.user),
    }
    return render(request, 'product-detail.html', context)

@login_required(login_url='/login/')
def room(request, slug):
    auction = Auction.objects.get(item__slug=slug)
    item = auction.item
    cart = Item.objects.filter(buyer=request.user)
    d = auction.cap_time
    print(d.strftime('%H:%M'))
    return render(request, 'auction.html', {
        'auction': auction,
        'room_name': auction.id,
        'user': request.user,
        'item': item,
        'deadline': auction.cap_time,
        'cart': cart,
    })


def addProduct(request):
    if request.method == 'POST':
        d1 = {key:request.POST[key] for key in ["item_name", "item_description", "condition", "base_price", "category"]}
        d2 = {key:request.POST[key] for key in ["start", "cap_time"]}
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
    image={}
    products = Item.objects.filter(seller = request.user.id)
    for p in products:
        image[p.id]=Image.objects.filter(item = p.id).first().image.url
    print(image)
    status = Item.STATUS
    return render(request, 'shopping-cart.html', {'form1': form1, 'form2': form2, 'products':products, 'status':status, 'image':image})

def shop(request):
    categories= Category.objects.all()
    items = Item.objects.all()
    print(items)
    # Query / Search Feature
    query = request.GET.get("q")
    if query:
        items = items.filter(
            Q(item_name__icontains=query)|
            Q(item_description__icontains=query)|            
            Q(condition__icontains=query)|
            Q(seller__first_name__icontains=query)|
            Q(category__category__icontains=query)
        ).distinct()
    items = list(items)
    live_items = []
    upcoming_items = []
    for item in items:
        if item.auction_status == "live":
            live_items.append(item)
        elif item.auction_status == "upcoming":
            upcoming_items.append(item)
    live_items.sort(key=Item.time_to_end, reverse=True)
    upcoming_items.sort(key=Item.time_to_start, reverse=True)
    items = live_items + upcoming_items
    paginator = Paginator(items, 12) 
    page = request.GET.get('page', 1)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list" : queryset,
        'categories':categories,
        'items':queryset,
        'cart': Item.objects.filter(buyer=request.user),
        'pages':paginator.num_pages,
        'current': int(page),
        'query':query,
    }
    return render(request, "product.html", context)


def cart(request):
    context = {
        'cart': Item.objects.filter(buyer=request.user),
    }
    return render(request, "cart.html", context)

def profile(request, id):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    user = User.objects.get(id=id)
    categories= Category.objects.all()
    items = Item.objects.all()
    print(items)
    items = list(items)
    live_items = []
    upcoming_items = []
    for item in items:
        if item.auction_status == "live":
            live_items.append(item)
        elif item.auction_status == "upcoming":
            upcoming_items.append(item)
    live_items.sort(key=Item.time_to_end, reverse=True)
    upcoming_items.sort(key=Item.time_to_start, reverse=True)
    items = live_items + upcoming_items
    paginator = Paginator(items, 12) 
    page = request.GET.get('page', 1)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        'user':user,
        "object_list" : queryset,
        'categories':categories,
        'items':queryset,
        'cart': Item.objects.filter(buyer=request.user),
        'pages':paginator.num_pages,
        'current': int(page),
    }

    if user == request.user:
        form = UserForm(instance = request.user)
        context["form"] = form

    return render(request,"profile.html", context)
