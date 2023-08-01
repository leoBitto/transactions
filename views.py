from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
def financial_summary(request):
    if request.method == 'POST':
        # Se il form è stato inviato via POST, accedi ai dati inviati dal form
        start_date = request.POST.get('startDate')  # Assumi che l'input del form abbia il nome 'startDate'
        end_date = request.POST.get('endDate')  # Assumi che l'input del form abbia il nome 'endDate'
    else:
        # Se la richiesta non è una POST, usa delle date di default o gestisci il caso come desideri
        start_date = '2023-01-01'
        end_date = '2023-12-31'

    # Filtra le entrate e le spese utilizzando le date specificate o quelle di default
    incomes = Income.objects.filter(date__range=[start_date, end_date])
    expenditures = Expenditure.objects.filter(date__range=[start_date, end_date])

    # Stampa i dati a fini di debugging
    print("start_date:", start_date)
    print("end_date:", end_date)
    print("incomes:", incomes)
    print("expenditures:", expenditures)

    context = {
        'incomes': incomes,
        'expenditures': expenditures,
    }

    # Restituisci la risposta rendendo il template 'transactions/Transactions.html'
    return render(request, 'transactions/Transactions.html', context)
@login_required
def base(request):
    return render(request, 'transactions/form.html', {})