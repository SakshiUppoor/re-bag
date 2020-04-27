from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from .forms import *
import datetime
from django.utils import timezone
from .models import *
# Create your views here.


# def createProduct(request):
#     if request.method == 'POST':
#         i = ItemForm(request.POST)
#         i.save()
#         a = AuctionForm(request.POST)
#         a.save()
#     else:
#         form1 = ItemForm()
#         form2 = AuctionForm()

#         context = {
#             'form1': form1,
#             'form2': form2,
#         }

#     return render(request, 'add_product.html', context)


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

def addProduct(request):
    if request.method == 'POST':
        d1 = {key:request.POST[key] for key in ["item_name", "item_description", "condition", "base_price", "cat"]}
        d2 = {key:request.POST[key] for key in ["start", "cap"]}
        print(d1)
        print(d2)
        form1 = ProductForm(d1)
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
        form1 = ProductForm()
        form2 = AuctionForm()
    return render(request, 'base.html', {'form1': form1, 'form2': form2})
