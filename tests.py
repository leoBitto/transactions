from django.test import TestCase
from .models import BankAccount, Cash, Income, Expenditure

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.bank_account = BankAccount.objects.create(bank_name='Test Bank', balance=1000)
        self.cash = Cash.objects.create(amount=500)
    
    def test_bank_account_creation(self):
        bank_account = BankAccount.objects.get(bank_name='Test Bank')
        self.assertEqual(bank_account.balance, 1000)
        
    def test_cash_creation(self):
        cash = Cash.objects.get(amount=500)
        self.assertEqual(cash.amount, 500)
    
    def test_income_creation(self):
        income = Income.objects.create(date='2023-08-01', amount=200, description='Test Income', bank_account=self.bank_account, type='Salary')
        self.assertEqual(income.amount, 200)
        self.assertEqual(income.bank_account, self.bank_account)
    
    def test_expenditure_creation(self):
        expenditure = Expenditure.objects.create(date='2023-08-01', amount=50, description='Test Expenditure', cash=self.cash, type='Food')
        self.assertEqual(expenditure.amount, 50)
        self.assertEqual(expenditure.cash, self.cash)
