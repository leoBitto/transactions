from django.contrib import admin
from .models import *


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'balance')
    search_fields = ('bank_name',)


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


admin.site.register(BalanceLog, BalanceLogAdmin)
admin.site.register(AmountLog, AmountLogAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Cash, CashAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)

