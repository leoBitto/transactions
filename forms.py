from django import forms
from .models import *
from django.forms.widgets import SelectDateWidget

class RecurringTransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    frequency = forms.ChoiceField(choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ])
    type = forms.ChoiceField(choices=[
        ('income', 'Income'),
        ('expense', 'Expense'),
    ])
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget, required=False)
    description = forms.CharField(max_length=100, required=False)
    payment_method = forms.CharField()
    income_type = forms.ChoiceField(choices=Income.Choices)
    expenditure_type = forms.ChoiceField(choices=Expenditure.Choices)


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'description', 'type', 'bank_account', 'cash']


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['date', 'amount', 'description', 'type', 'bank_account', 'cash']


class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    bank_account = forms.ModelChoiceField(queryset=BankAccount.objects.all())