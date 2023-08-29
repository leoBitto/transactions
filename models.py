from django.db import models
from datetime import date


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account.name} - {self.bank_name}"


class Cash(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account.name} - Cash"


class Transaction(models.Model):
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccount, null=True, blank=True, on_delete=models.CASCADE)
    cash = models.ForeignKey(Cash, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaction: {self.amount} on {self.date}"

class Income(Transaction):
    Choices =[
        ('Savings','Savings'),
        ('Salary','Salary'),
        ('Bonus','Bonus'),
        ('Dividends','Dividends'),
        ('Other','Other'),
    ]
    type=models.CharField(choices=Choices, max_length=10)

    def __str__(self):
        return f"Income: {self.amount} on {self.date}"


class Expenditure(Transaction):
    Choices =[
        ('Food','Food'),
        ('Gifts','Gifts'),
        ('Health','Health'),
        ('House','House'),
        ('Transport','Transport'),
        ('Personal Expense','Personal Expense'),
        ('Bills','Bills'),
        ('Trip','Trip'),
        ('Debts','Debts'),
        ('Other','Other'),
    ]
    type=models.CharField(choices=Choices, max_length=16)

    def __str__(self):
        return f"Expenditure: {self.amount} on {self.date}"


class Asset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    initial_value = models.DecimalField(max_digits=10, decimal_places=2)
    annual_depreciation = models.DecimalField(max_digits=10, decimal_places=2)
    acquisition_date = models.DateField()

    def residual_value(self):
        years_passed = (date.today() - self.acquisition_date).days / 365
        residual_value = self.initial_value - (self.annual_depreciation * years_passed)
        return residual_value

    def __str__(self):
        return self.name


class Liability(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    debt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class CashFlow(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.name







