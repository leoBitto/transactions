from django.db import models

# Create your models here.
class Transaction(models.Model):
    date= models.DateField()
    amount = models.FloatField()
    description=models.CharField(max_length=100)


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