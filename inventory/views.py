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
    return render(request, "home.html", context)

@login_required
def list_items(request):
    title = 'List Of Items'
    form = StockSearchForm(request.POST or None)
    stockList = Stock.objects.all()

    if request.method == 'POST':
        category = form['category'].value()
        item_name = form['item_name'].value()
        stockList = Stock.objects.filter(category__name__icontains=category, item_name__icontains=item_name)

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

        # Check if the category already exists
        existing_category, created = Category.objects.get_or_create(name=category_name)

        # Create the new item with the existing or new category
        Stock.objects.create(item_name=item_name, category=existing_category)

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
            return redirect('list_items')  # Use the named URL 'list_items'

    context = {
        'form': form,
    }
    return render(request, 'add_items.html', context)

@login_required
def delete_item(request, pk):
    stock_instance = get_object_or_404(Stock, id=pk)
    
    if request.method == 'POST':
        stock_instance.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('/list_items')  # Use the named URL 'list_items'
    
    return render(request, 'delete_item.html')

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
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)

@login_required
def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
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