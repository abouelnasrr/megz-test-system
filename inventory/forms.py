from django import forms
from .models import StockWarning
from shop.models import Products

class StockWarningForm(forms.ModelForm):
    class Meta:
        model = StockWarning
        fields = ['product', 'warning_limit']
