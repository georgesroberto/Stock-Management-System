from django.shortcuts import render, redirect
from .models import *
from .forms import StockCreateForm
# Create your views here.

def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        "title": title,
	}
    return render(request, "home.html",context)


def list_items(request):
    header = 'Welcome: View Items List'
    listss = Stock.objects.all()

    context = {
        "get_header" : header,
        "items" : listss

    }

    return render(request, 'list_items.html', context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_item')

    context = {
        "form" : form,
        "title" : "Add Item",
    }
    
    return render(request, 'add_items.html', context)