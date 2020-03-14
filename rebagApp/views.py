from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
    print(item.item_images.first())
    return render(request, 'auction.html', {
        'room_name': room_name,
        'user': request.user,
        'item': item,
    })
