import datetime
from django import forms

from transaction.models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields =['amount', 'details', 'date', 'transaction_type']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Details'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        pass

class TransactionUpdateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'details', 'date', 'transaction_type']



        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Details'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transaction_type':forms.Select(attrs={'class': 'form-select'}),
        }
