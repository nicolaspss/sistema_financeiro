from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

def accounts(request):
    if request.user.is_authenticated:
        accounts = BankAccounts.objects.all()
        return render(request, 'accounts/accounts.html', {"accounts": accounts})
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        redirect('home')

def add_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            account = BankAccounts()
            account.name = request.POST.get('name')
            account.account_type = request.POST.get('account_type')
            account.account_number = request.POST.get('account_number')
            account.agency = request.POST.get('agency')
            account.titular_name = request.POST.get('titular_name')
            account.titular_document = request.POST.get('titular_document')
            account.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('accounts')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def update_account(request, pk):
    if request.user.is_authenticated:
        account = BankAccounts.objects.get(id=pk)
        account.name = request.POST.get('name')
        account.account_type = request.POST.get('account_type')
        account.account_number = request.POST.get('account_number')
        account.agency = request.POST.get('agency')
        account.titular_name = request.POST.get('titular_name')
        account.titular_document = request.POST.get('titular_document')
        account.save()
        messages.success(request, "Record updated successfully!")
        return redirect('accounts')
    else:
        messages.success(request, "You must be logged in.")
        return redirect('home')
    
def delete_account(request, pk):
    if request.user.is_authenticated:
        delete_it = BankAccounts.objects.get(id=pk) #O método get() pega no banco de dados através do ID.
        delete_it.delete()
        messages.success(request, "Cadastro deletado com sucesso!")
        return redirect('accounts')
    else:
        messages.success(request, "Você não tem permissão para fazer modificações. Contate o Administrador do sistema.")
        return redirect('home')