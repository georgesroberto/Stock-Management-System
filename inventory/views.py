from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
import csv

def home(request):
    title = 'Welcome: This is the Home Page'
    context = {"title": title}
    return render(request, 'home.html/', context)


@login_required
def list_items(request):
    title = 'List Of Items'
    form = StockSearchForm(request.POST or None)
    stockList = Stock.objects.all()

    if request.method == 'POST':
        category = request.POST.get('category')
        item_name = request.POST.get('item_name')
        queryset = StockHistory.objects.filter(item_name__icontains=form['item_name'].value())

        if (category != ''):
            queryset = queryset.filter(category_id=category)

        stockList = queryset
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


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)

    if form.is_valid():
        item_name = form.cleaned_data['item_name']
        category_name = form.cleaned_data['category']
        quantity = form.cleaned_data['quantity']

        existing_category, created = Category.objects.get_or_create(name=category_name)

        Stock.objects.create(item_name=item_name, category=existing_category, quantity=quantity)
        messages.success(request, 'Successfully Saved')
        
        return redirect('list_items')

    context = {
        "form": form,
        "title": "Add Item",
    }

    return render(request, 'add_items.html', context)
    

@login_required
def update_item(request, pk):
    stockList = get_object_or_404(Stock, id=pk)
    form = StockUpdateForm(instance = stockList)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=stockList)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('list_items') 

    context = {
        'form': form,
    }
    return render(request, 'add_items.html', context)


@login_required
def delete_item(request, pk):
    stock_instance = get_object_or_404(Stock, id=pk)
    
    if request.method == 'POST':
        item_name = stock_instance.item_name
        stock_instance.delete()
        messages.success(request, f'Successfully Deleted: {item_name} ')
        return redirect('/list_items')  
    
    return render(request, 'delete_item.html', {'stock_instance': stock_instance})


@login_required
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issued By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now in Store")
        
        return redirect('/stock_detail/' + str(instance.id))

    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Received By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


@login_required
def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)


@login_required
def list_history(request):  
    header = 'History Data'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)

    context = {
		"header": header,
		"queryset": queryset,
        "form" : form,
	}

    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(item_name__icontains=form['item_name'].value())

        if (category != ''):
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
				['CATEGORY', 
				'ITEM NAME',
				'QUANTITY', 
				'ISSUED QUANTITY', 
				'RECEIVED QUANTITY', 
				'RECEIVED BY', 
				'ISSUED BY', 
				'LAST UPDATED'])
            instance = queryset
            
            for stock in instance:
                writer.writerow(
			    [stock.category, 
				stock.item_name, 
				stock.quantity, 
				stock.issue_quantity, 
				stock.receive_quantity, 
				stock.receive_by, 
				stock.issue_by, 
				stock.last_updated])
            return response
    
        context = {
            "header": header,
            "queryset": queryset,
            "form" : form, 
	    }
    return render(request, "list_history.html",context)