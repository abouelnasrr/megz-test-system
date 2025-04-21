from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'expense_type', 'amount', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
