from django import forms
from .models import Stock, StockHistory

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')

        if Stock.objects.filter(item_name=item_name).exists():
            raise forms.ValidationError('An item with this name already exists.')

        return item_name  

class StockSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required = False)
   class Meta:
        model = Stock
        fields = ['category', 'item_name']
		
class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
	class Meta:
		model = StockHistory
		fields = ['category', 'item_name', 'start_date', 'end_date']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity']
          
class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']
  
class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']