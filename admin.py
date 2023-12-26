from django.contrib import admin
from .models import *


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')
    search_fields = ('name',)


class CashAdmin(admin.ModelAdmin):
    list_display = ('amount',)
    search_fields = ('amount',)


class BalanceLogAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'balance', 'timestamp')
    list_filter = ('bank_account', 'timestamp')
    search_fields = ('bank_account__account_number', 'timestamp')


class AmountLogAdmin(admin.ModelAdmin):
    list_display = ('cash', 'amount', 'timestamp')
    list_filter = ('cash', 'timestamp')
    search_fields = ('cash__description', 'timestamp')


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'type', 'bank_account', 'cash')
    list_filter = ('date', 'type', 'bank_account', 'cash')
    search_fields = ('description', 'type')
    raw_id_fields = ('bank_account', 'cash')


class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'type', 'bank_account', 'cash')
    list_filter = ('date', 'type', 'bank_account', 'cash')
    search_fields = ('description', 'type')
    raw_id_fields = ('bank_account', 'cash')

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock_value', 'total_value')
    search_fields = ('name',)
    list_filter = ('start_date',)
    readonly_fields = ('stock_value', 'total_value',)

class StockInPortfolioAdmin(admin.ModelAdmin):
    list_display = (
        #'company', 
        'related_portfolio', 'quantity', 'price')
    search_fields = ('company__name', 'related_portfolio__name')

class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('stock', 'transaction_type', 'quantity', 'price', 'commission', 'transaction_date')
    search_fields = ('stock__company__name', 'transaction_type')
    list_filter = ('transaction_date',)



admin.site.register(BalanceLog, BalanceLogAdmin)
admin.site.register(AmountLog, AmountLogAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Cash, CashAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(StockInPortfolio, StockInPortfolioAdmin)
admin.site.register(StockTransaction, StockTransactionAdmin)

