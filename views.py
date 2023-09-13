from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from django.contrib import messages
from datetime import date
from decimal import Decimal
import logging
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def financial_summary(request):
    if request.method == 'POST':
        # Se il form è stato inviato via POST, accedi ai dati inviati dal form
        start_date = request.POST.get('startDate')  # Assumi che l'input del form abbia il nome 'startDate'
        end_date = request.POST.get('endDate')  # Assumi che l'input del form abbia il nome 'endDate'
    else:
        # Se la richiesta non è una POST, usa delle date di default 
        start_date = '2023-01-01'
        end_date = '2023-12-31'

    # Filtra le entrate e le spese utilizzando le date specificate o quelle di default
    incomes = Income.objects.filter(date__range=[start_date, end_date]).order_by('-date', 'amount')
    expenditures = Expenditure.objects.filter(date__range=[start_date, end_date]).order_by('-date', 'amount')

    # Converti i risultati della query in un DataFrame
    incomes_data = list(incomes.values('date', 'amount', 'type'))
    incomes_df = pd.DataFrame(incomes_data)

    # Esegui lo stesso processo per le uscite
    expenditures_data = list(expenditures.values('date', 'amount', 'type'))
    expenditures_df = pd.DataFrame(expenditures_data)

    # Verifica se ci sono dati validi per i grafici
    if not incomes_df.empty:
        # Crea e visualizza il grafico a torta per le categorie di entrate
        fig_pie_income = px.pie(incomes_df, names='type', values='amount', title='Distribution of Income Categories')
        html_pie_income = pio.to_html(fig_pie_income)
    else:
        html_pie_income = "No income data available"

    if not expenditures_df.empty:
        # Crea e visualizza il grafico a torta per le categorie di uscite
        fig_pie_expenditure = px.pie(expenditures_df, names='type', values='amount', title='Distribution of Expenditure Categories')
        html_pie_expenditure = pio.to_html(fig_pie_expenditure)
    else:
        html_pie_expenditure = "No expenditure data available"

    if not incomes_df.empty:
        # Calcola le somme totali delle entrate per ogni giorno
        total_incomes_per_day = incomes_df.groupby('date')['amount'].sum().reset_index()

        # Crea e visualizza il grafico a linee per le entrate nel tempo
        fig_line_income = px.line(incomes_df, x='date', y='amount', color='type', title='Income Over Time')
        # Aggiungi la linea delle entrate totali
        fig_line_income.add_trace(go.Scatter(x=total_incomes_per_day['date'], y=total_incomes_per_day['amount'],
                                     mode='lines+markers', name='Total Income'))
        html_line_income = pio.to_html(fig_line_income)
    else:
        html_line_income = "No income data available"

    if not expenditures_df.empty:
        # Calcola le somme totali delle entrate per ogni giorno
        total_expenses_per_day = expenditures_df.groupby('date')['amount'].sum().reset_index()

        # Crea e visualizza il grafico a linee per le entrate nel tempo
        fig_line_expenditure = px.line(expenditures_df, x='date', y='amount', color='type', title='Expenses Over Time')
        # Aggiungi la linea delle entrate totali
        fig_line_expenditure.add_trace(go.Scatter(x=total_expenses_per_day['date'], y=total_expenses_per_day['amount'],
                                     mode='lines+markers', name='Total Expenses'))
        html_line_expenditure = pio.to_html(fig_line_expenditure)
    else:
        html_line_expenditure = "No expenditure data available"


    logger.debug("start_date: %s", start_date)
    logger.debug("end_date: %s", end_date)
    logger.debug("incomes: %s", incomes)
    logger.debug("expenditures: %s", expenditures)
    logger.debug("incomes_df: %s", incomes_df)
    logger.debug("expenditures_df: %s", expenditures_df)

    context = {
        'incomes': incomes,
        'expenditures': expenditures,
        'fig_pie_income':html_pie_income,
        'fig_pie_expenditure':html_pie_expenditure,
        'fig_line_income':html_line_income,
        'fig_line_expenditure':html_line_expenditure,
        'income_form': IncomeForm(),
        'expenditure_form': ExpenditureForm(),
        'today': date.today().strftime('%Y-%m-%d')
    }

    # Restituisci la risposta rendendo il template 'transactions/Transactions.html'
    return render(request, 'transactions/Transactions.html', context)


@login_required
def transaction_registration(request):
    if request.method == 'POST':
        income_form = IncomeForm(request.POST)
        expenditure_form = ExpenditureForm(request.POST)

        if income_form.is_valid():
            # Gestione delle entrate
            income = income_form.save(commit=False)  # Non salvare subito nel database

            # Controlla se esiste un guadagno simile nello stesso giorno e dello stesso tipo
            existing_income = Income.objects.filter(date=income.date, type=income.type).first()

            if existing_income:
                # Aggiorna l'importo del guadagno esistente
                existing_income.amount += Decimal(str(income.amount))
                existing_income.save()
            else:
                # Crea una nuova voce nel database per il guadagno
                income.save()

            # Aggiorna il saldo del conto bancario associato
            if income.bank_account:
                bank_account = BankAccount.objects.get(pk=income.bank_account.pk)
                bank_account.balance += Decimal(str(income.amount))
                bank_account.save()

            # Aggiorna l'entità cash se presente
            if income.cash:
                cash = Cash.objects.get(pk=income.cash.pk)
                cash.amount += Decimal(str(income.amount))
                cash.save()

            return redirect('transactions:financial_summary')

        if expenditure_form.is_valid():
            # Gestione delle spese
            expenditure = expenditure_form.save(commit=False)  # Non salvare subito nel database

            # Controlla se la spesa porta il saldo del conto o del contante a un valore negativo
            if expenditure.bank_account:
                bank_account = BankAccount.objects.get(pk=expenditure.bank_account.pk)
                if bank_account.balance - expenditure.amount < 0:
                    messages.error(request, "La spesa supera il saldo disponibile.")
                    return redirect('transactions:financial_summary')

            if expenditure.cash:
                cash = Cash.objects.get(pk=expenditure.cash.pk)
                if cash.amount - Decimal(str(expenditure.amount)) < 0:
                    messages.error(request, "La spesa supera il saldo cash disponibile.")
                    return redirect('transactions:financial_summary')


            # Controlla se esiste una spesa simile nello stesso giorno e dello stesso tipo
            existing_expenditure = Expenditure.objects.filter(date=expenditure.date, type=expenditure.type).first()

            if existing_expenditure:
                # Aggiorna l'importo della spesa esistente
                existing_expenditure.amount += Decimal(str(expenditure.amount))
                existing_expenditure.save()
            else:
                # Crea una nuova voce nel database per la spesa
                expenditure.save()

            # Aggiorna il saldo del conto bancario associato
            if expenditure.bank_account:
                bank_account = BankAccount.objects.get(pk=expenditure.bank_account.pk)
                bank_account.balance -= Decimal(str(expenditure.amount))
                bank_account.save()

            # Aggiorna l'entità cash se presente
            if expenditure.cash:
                cash = Cash.objects.get(pk=expenditure.cash.pk)
                cash.amount -= Decimal(str(expenditure.amount))
                cash.save()

            return redirect('transactions:financial_summary')

    return redirect('transactions:financial_summary')


@login_required
def base(request):
    today = date.today()
    future_expenses = Expenditure.objects.filter(date__gt=today)
    
    for expense in future_expenses:
        # Esempio: Se la data è entro una settimana dalla data odierna, considera la spesa urgente
        if (expense.date - today).days <= 7:
            expense.is_urgent = True

    bank_accounts = BankAccount.objects.all()
    cash = Cash.objects.all()[0]
    
    total_savings = sum([account.balance for account in bank_accounts]) + cash.amount

    context = {
        'future_expenses':future_expenses,
        'cash':cash,
        'bank_accounts': bank_accounts,
        'total_savings': total_savings,
    }
    
    return render(request, 'transactions/form.html', context)

@login_required
def bank_detail(request, pk):
    bank_account = get_object_or_404(BankAccount, pk=pk)
    bank_accounts = BankAccount.objects.exclude(pk=pk)

    if request.method == 'POST':
        if 'transfer_button' in request.POST:
            target_account_name = request.POST.get('target_account')
            amount = Decimal(request.POST.get('amount'))
            commission = Decimal(request.POST.get('commission'))
            
            try:
                target_account = BankAccount.objects.get(bank_name=target_account_name)
            except BankAccount.DoesNotExist:
                raise Http404("L'account bancario di destinazione non esiste.")

            if bank_account.transfer_money(target_account, amount, commission):
                messages.success(request, 'Il trasferimento è avvenuto con successo.')
            else:
                messages.error(request, 'Il trasferimento non è riuscito.')

        elif 'retire_button' in request.POST:
            retire_amount = Decimal(request.POST.get('retire_amount'))
            retire_commission = Decimal(request.POST.get('retire_commission'))
            
            if bank_account.withdraw_money(retire_amount, retire_commission):
                messages.success(request, 'Il ritiro è avvenuto con successo.')
            else:
                messages.error(request, 'Il ritiro non è riuscito.')

        return redirect('transactions:bank_detail', pk=pk)
    

    balance_logs = BalanceLog.objects.filter(bank_account=bank_account)

    df = pd.DataFrame(list(balance_logs.values()))
    print(df)
    # Verifica se il DataFrame df è vuoto
    if not df.empty:
        fig = px.line(df, x='timestamp', y='balance', title='Balance Over Time')
        fig.update_xaxes(title_text='Timestamp')
        fig.update_yaxes(title_text='Balance')

        # Genera il grafico Plotly e il codice HTML solo se il DataFrame non è vuoto
        html_fig = pio.to_html(fig)
    else:
        # DataFrame vuoto, imposta html_fig a una stringa vuota o un messaggio di avviso
        html_fig = "<p class='m-4'>No record to show</p>"

    context = {
        'bank_account': bank_account, 
        'bank_accounts': bank_accounts,
        'html_fig':html_fig,
    }

    return render(request, 'transactions/bank_detail.html', context)


@login_required
def cash_detail(request, pk):
    cash_account = get_object_or_404(Cash, pk=pk)

    amount_logs = AmountLog.objects.all()

    df = pd.DataFrame(list(amount_logs.values()))

    # Verifica se il DataFrame df è vuoto
    if not df.empty:
        fig = px.line(df, x='timestamp', y='amount', title='Amount Over Time')
        fig.update_xaxes(title_text='Timestamp')
        fig.update_yaxes(title_text='Amount')

        # Genera il grafico Plotly e il codice HTML solo se il DataFrame non è vuoto
        html_fig = pio.to_html(fig)
    else:
        # DataFrame vuoto, imposta html_fig a una stringa vuota o un messaggio di avviso
        html_fig = "<p class='m-4'>No record to show</p>"

    context = {
        'cash_account': cash_account,
        'html_fig':html_fig,
        }

    return render(request, 'transactions/cash_detail.html', context)



@login_required
def create_recurring_transaction(request):
    # Ottieni gli account bancari e l'entità Cash dal database
    bank_accounts = BankAccount.objects.all()
    cash_entity = Cash.objects.all()[0]  # Assumendo che ci sia solo un oggetto Cash nel database

    income_choices = Income.Choices
    expenditure_choices = Expenditure.Choices

    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            # Eseguire il salvataggio manuale dei dati del form
            amount = form.cleaned_data['amount']
            frequency = form.cleaned_data['frequency']
            transaction_type = form.cleaned_data['type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            description = form.cleaned_data['description']
            payment_method = form.cleaned_data['payment_method']
            income_type = form.cleaned_data['income_type']
            expenditure_type = form.cleaned_data['expenditure_type']
            
            if payment_method == 'cash':
                selected_cash_entity = cash_entity
                selected_bank_account = None
            else:
                selected_bank_account = BankAccount.objects.get(pk=payment_method)
                selected_cash_entity = None

            # Verifica se la data di fine è stata fornita
            if end_date and end_date >= date.today():
                _, days_in_start_month = monthrange(start_date.year, start_date.month)
                delta = end_date - start_date
                total_days = delta.days

                if frequency == 'daily':
                    increment = timedelta(days=1)
                elif frequency == 'weekly':
                    increment = timedelta(weeks=1)
                elif frequency == 'monthly':
                    increment = timedelta(days=days_in_start_month)
                elif frequency == 'annual':
                    _, days_in_year = monthrange(start_date.year, 12)
                    increment = timedelta(days=days_in_year)
                else:
                    increment = None
                    total_days = 0

                for i in range(total_days):
                    new_date = start_date + i * increment
                    _, days_in_month = monthrange(new_date.year, new_date.month)

                    if new_date.day > days_in_month:
                        new_date = new_date.replace(day=days_in_month)

                    if transaction_type == 'income':
                        new_transaction = Income(
                            date=new_date,
                            amount=amount,
                            description=description,
                            bank_account=selected_bank_account,
                            cash=selected_cash_entity,
                            type=income_type,
                        )
                    else:
                        new_transaction = Expenditure(
                            date=new_date,
                            amount=amount,
                            description=description,
                            bank_account=selected_bank_account,
                            cash=selected_cash_entity,
                            type=expenditure_type,
                        )

                    new_transaction.save()

            elif not end_date:
                # Se la data di fine non è stata fornita, crea una sola transazione
                if transaction_type == 'income':
                    new_transaction = Income(
                        date=start_date,
                        amount=amount,
                        description=description,
                        bank_account=bank_accounts.first(),  # Cambia con l'account bancario corretto
                        cash=cash_entity,
                        type=expenditure_type,
                    )
                else:
                    new_transaction = Expenditure(
                        date=start_date,
                        amount=amount,
                        description=description,
                        bank_account=bank_accounts.first(),  # Cambia con l'account bancario corretto
                        cash=cash_entity,
                        type=expenditure_type,
                    )

                new_transaction.save()

            return redirect('transactions:financial_summary')
    else:
        form = RecurringTransactionForm()

    context = {
        'form': form, 
        'bank_accounts': bank_accounts, 
        'cash_entity': cash_entity,
        'income_choices': income_choices,
        'expenditure_choices': expenditure_choices
        }
    return render(request, 'transactions/recurring_transaction.html', context)
