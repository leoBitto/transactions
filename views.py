from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Create your views here.
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

    # Grafico a Torta per le Categorie di Entrate
    fig_pie_income = px.pie(incomes_df, names='type', values='amount', title='Distribution of Income Categories')

    # Grafico a Torta per le Categorie di Uscite
    fig_pie_expenditure = px.pie(expenditures_df, names='type', values='amount', title='Distribution of Expenditure Categories')

    # Grafico a Linee per le Entrate nel Tempo
    fig_line_income = px.line(incomes_df, x='date', y='amount', color='type', title='Income Over Time')

    # Grafico a Linee per le Uscite nel Tempo
    fig_line_expenditure = px.line(expenditures_df, x='date', y='amount', color='type', title='Expenditure Over Time')

    html_pie_income = pio.to_html(fig_pie_income)
    html_pie_expenditure = pio.to_html(fig_pie_expenditure)
    html_line_income = pio.to_html(fig_line_income)
    html_line_expenditure = pio.to_html(fig_line_expenditure)

    # Stampa i dati a fini di debugging
    print("start_date:", start_date)
    print("end_date:", end_date)
    print("incomes:", incomes)
    print("expenditures:", expenditures)
    print("incomes_df:", incomes_df)
    print("expenditures_df:", expenditures_df)

    context = {
        'incomes': incomes,
        'expenditures': expenditures,
        'fig_pie_income':html_pie_income,
        'fig_pie_expenditure':html_pie_expenditure,
        'fig_line_income':html_line_income,
        'fig_line_expenditure':html_line_expenditure,
    }

    # Restituisci la risposta rendendo il template 'transactions/Transactions.html'
    return render(request, 'transactions/Transactions.html', context)



@login_required
def base(request):
    return render(request, 'transactions/form.html', {})