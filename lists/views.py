from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from models import Item, List


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(
        text=request.POST.get('item_text'),
        list=list_
    )

    path = reverse('view_list', kwargs={'list_id': list_id})
    return redirect(path)

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)

    path = reverse('view_list', kwargs={'list_id': list_.id})
    return redirect(path)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)

    return render(request, 'list.html', {'items': items, 'list': list_})