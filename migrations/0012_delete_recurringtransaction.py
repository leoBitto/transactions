# Generated by Django 4.1.7 on 2023-09-13 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_bankaccount_start_date_cash_start_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecurringTransaction',
        ),
    ]
