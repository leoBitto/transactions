from django.db import models
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from calendar import monthrange

class BankAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()

    # funzione per trasferire denaro da questo account a un altro account bancario
    def transfer_money(self, target_account, amount, commision):
        if self.balance >= (amount + commision):
            self.balance -= (amount + commision)
            target_account.balance += amount
            self.save()
            target_account.save()
            return True
        return False

    # funzione per ritirare denaro dall'account
    def withdraw_money(self, amount, commision):
        if self.balance >= (amount + commision):
            self.balance -= amount
            cash = Cash.objects.all()[0]
            cash.amount += amount
            self.save()
            cash.save()
            return True
        return False

    @property
    def total_balance(self):
        today = date.today()
        transactions = self.transactions.filter(processed_date__range=(self.start_date, today))
        return sum(transactions.values_list('amount', flat=True))

    def __str__(self):
        return f"{self.bank_name}"
    

class Cash(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()

    @property
    def total_amount(self):
        today = date.today()
        transactions = self.transactions.filter(processed_date__range=(self.start_date, today))
        return sum(transactions.values_list('amount', flat=True))

    def __str__(self):
        return f"{self.amount} - Cash"


class BalanceLog(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class AmountLog(models.Model):
    cash = models.ForeignKey(Cash, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=BankAccount)
def log_balance_change(sender, instance, created, **kwargs):
    if not created:
        BalanceLog.objects.create(bank_account=instance, balance=instance.balance)

@receiver(post_save, sender=Cash)
def log_amount_change(sender, instance, created, **kwargs):
    if not created:
        AmountLog.objects.create(cash=instance, amount=instance.amount)



class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)
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


class InvestmentAccount(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    portfolio = models.ForeignKey('screener.Portfolio', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Investment Account: {self.account.bank_name}"








