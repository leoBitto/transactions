from django import forms
from .models import *
from django.forms.widgets import SelectDateWidget
try:
    from screener.models import Company
except ModuleNotFoundError:
    Company = None  # O qualsiasi altro gestore che desideri in caso di mancanza dell'applicazione


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


class AddBankForm(forms.Form):
    name = forms.CharField()
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        

class AddCashAmountForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
 
class TransactionStockForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    commission = forms.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Aggiunto widget
    transaction_type = forms.ChoiceField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')])


class ManageCashForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = forms.ChoiceField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')])
    commission = forms.DecimalField(max_digits=10, decimal_places=2)






