from django.contrib import admin
from .models import *



class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'type')
    list_filter = ('type', 'date')
    search_fields = ('description', 'type')


class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'type')
    list_filter = ('type', 'date')
    search_fields = ('description', 'type')



admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)