from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

def transfers(request):
    if request.user.is_authenticated:
        transfers = Transfer.objects.all().order_by('-id')[:50]
        accounts = Account.objects.all()
        bank_accounts = BankAccounts.objects.all()
        suppliers = Supplier.objects.all()
        sum_transfer=Transfer.objects.aggregate(Sum('value'))
        return render(request, 'transfers/transfers.html', {
            'transfers': transfers,
            'accounts': accounts,
            'bank_accounts': bank_accounts,
            'suppliers': suppliers,
            'transfer_sum': sum_transfer,
        })
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')

def filter_by_date(request):
    if request.user.is_authenticated:
        start = request.GET.get('start')
        end = request.GET.get('end')
        transfers = Transfer.objects.filter(end_date__range=(start, end))
        sum_transfer = Transfer.objects.filter(end_date__range=(start, end)).aggregate(Sum('value'))
        return render(request, 'transfers/transfers_search.html', {
            'transfers': transfers,
            'transfer_sum': sum_transfer,
        })
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def search_filter(request):
    pass

def add_new_receipt(request):   
    if request.user.is_authenticated:
        if request.method == "POST":
            value = request.POST.get('value')
            supplier_id = request.POST.get('supplier')
            supplier = Supplier.objects.get(id=supplier_id)
            account_id = request.POST.get('account')
            account = Account.objects.get(id=account_id)
            bank_id = request.POST.get('bank_account')
            bank = BankAccounts.objects.get(id=bank_id)
            transfer_type = "Recebimento"
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            transfer = Transfer(value=value, 
                                supplier=supplier, 
                                account=account, 
                                bank_account=bank, 
                                start_date=start_date, 
                                end_date=end_date, 
                                transfer_type=transfer_type)
            messages.success(request, "Cadastro realizado com sucesso!")
            transfer.save()
            return redirect('transfers')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def add_new_payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            value = float(request.POST.get('value'))
            negative = -abs(value)
            supplier_id = request.POST.get('supplier')
            supplier = Supplier.objects.get(id=supplier_id)
            account_id = request.POST.get('account')
            account = Account.objects.get(id=account_id)
            bank_id = request.POST.get('bank_account')
            bank = BankAccounts.objects.get(id=bank_id)
            transfer_type = "Pagamento"
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            transfer = Transfer(value=negative, 
                                supplier=supplier, 
                                account=account, 
                                bank_account=bank,
                                start_date=start_date, 
                                end_date=end_date,  
                                transfer_type=transfer_type)
            messages.success(request, "Cadastro realizado com sucesso!")
            transfer.save()
            return redirect('transfers')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def delete_transfer(request, pk):
    if request.user.is_authenticated:
        delete_it = Transfer.objects.get(id=pk) #O método get() pega no banco de dados através do ID.
        delete_it.delete()
        messages.success(request, "Cadastro deletado com sucesso!")
        return redirect('transfers')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')