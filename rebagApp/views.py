from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from .forms import *
# Create your views here.


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
