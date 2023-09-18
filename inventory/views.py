from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
from django.contrib import messages
import csv

def home(request):
    title = 'Welcome: This is the Home Page'
    context = {"title": title}
    return render(request, "home.html", context)

def list_items(request):
    title = 'List Of Items'
    form = StockSearchForm(request.POST or None)
    stockList = Stock.objects.all()

    if request.method == 'POST':
        category = form['category'].value()
        item_name = form['item_name'].value()
        stockList = Stock.objects.filter(category__icontains=category, item_name__icontains=item_name)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = stockList
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
    
    context = {
        "items": stockList,
        "title": title,
        "form": form,
    }

    return render(request, 'list_items.html', context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_items')  # Use the named URL 'list_items'

    context = {
        "form": form,
        "title": "Add Item",
    }
    
    return render(request, 'add_items.html', context)

def update_item(request, pk):
    stockList = get_object_or_404(Stock, id=pk)
    form = StockUpdateForm(instance = stockList)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=stockList)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('list_items')  # Use the named URL 'list_items'

    context = {
        'form': form,
    }
    return render(request, 'add_items.html', context)

def delete_item(request, pk):
    stock_instance = get_object_or_404(Stock, id=pk)
    
    if request.method == 'POST':
        stock_instance.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')  # Use the named URL 'list_items'
    
    return render(request, 'delete_item.html')
