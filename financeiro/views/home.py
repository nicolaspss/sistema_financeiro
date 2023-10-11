from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
import calendar
from django.db.models.functions import TruncMonth
from django.db.models.functions import Abs

# Início

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Seja bem vindo, {username}!")
            return redirect('home')
        else:
            messages.success(request, "Tente novamente!")
            return redirect('home')
        
    all_transfers = Transfer.objects.all().order_by('-id')[:5]
        
    current_year = datetime.now().year
    current_month = datetime.now().month
    last_month = datetime.now().month - 1

    last = calendar.monthrange(current_year, current_month)[1]
    last_month_day = calendar.monthrange(current_year, current_month - 1)[1]

    receipts_data = Transfer.objects.annotate(month_year=TruncMonth('start_date')).values('month_year').filter(transfer_type='Recebimento').annotate(total_value_receipt=Sum('value')).order_by('month_year')
    payments_data = Transfer.objects.annotate(month_year=TruncMonth('start_date')).values('month_year').filter(transfer_type='Pagamento').annotate(total_value_payment=Sum('value')).order_by('month_year')
    total_data = Transfer.objects.annotate(month_year=TruncMonth('start_date')).values('month_year').annotate(total_value=Sum('value')).order_by('month_year')
    
    receipts_month = Transfer.objects.filter(start_date__range=[f"{current_year}-{current_month}-01", f"{current_year}-{current_month}-{last}"], transfer_type='Recebimento').aggregate(Sum('value'))
    payments_month = Transfer.objects.filter(start_date__range=[f"{current_year}-{current_month}-01", f"{current_year}-{current_month}-{last}"], transfer_type='Pagamento').aggregate(Sum('value'))

    total_month = Transfer.objects.filter(start_date__range=[f"{current_year}-{current_month}-01", f"{current_year}-{current_month}-{last}"]).aggregate(Sum('value'))
    last_total = Transfer.objects.filter(start_date__range=[f"{current_year}-{last_month}-01", f"{current_year}-{last_month}-{last_month_day}"]).aggregate(Sum('value'))

    labels = [entry['month_year'].strftime('%Y-%m') for entry in total_data]

    data_1 = [float(entry['total_value_receipt']) for entry in receipts_data]
    data_2 = [float(entry['total_value_payment']) for entry in payments_data]
    data_3 = [float(entry['total_value']) for entry in total_data] # type: ignore

    print(last_total)

    return render(request, 'home.html', {'labels': labels, 
                                         'receipts_data': data_1, 
                                         'payments_data': data_2,
                                         'total_data': data_3,
                                         'receipts_month': receipts_month, 
                                         'payments_month': payments_month,
                                         'current_year': current_year,
                                         'current_month': current_month,
                                         'total_month': total_month,
                                         'last_total': last_total,
                                         'last_month': last_month,
                                         'all_transfers': all_transfers,})

def logout_user(request):
    logout(request)
    messages.warning(request, "Você foi desconectado.")
    return redirect('home')