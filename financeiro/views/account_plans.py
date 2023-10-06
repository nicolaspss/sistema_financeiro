from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

def account_plans(request):
    if request.user.is_authenticated:
        all_categories = Category.objects.all()
        return render(request, 'account_plan/account_plan.html', {"categories": all_categories})

def add_new_category(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            category = Category()
            category.name = request.POST.get('name')
            category.save()
            return redirect('account_plans')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def update_category(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            pass
            
def delete_category(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            category = request.POST.get('category')
            delete_it = Category.objects.get(id=category) #O método get() pega no banco de dados através do ID.
            delete_it.delete()
            messages.success(request, "Cadastro deletado com sucesso!")
            return redirect('account_plans')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')

def add_new_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('account_name')
            amount = Transfer.objects.filter(account='account_set').aggregate(Sum('value'))
            category_id = request.POST.get('account_category')
            category = Category.objects.get(id=category_id)
            account = Account(name=name, amount=amount, category=category)
            account.save()
            return redirect('account_plans')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def update_account_plan(request, pk):
    if request.user.is_authenticated:
        account = Account.objects.get(id=pk)
        if request.method == "POST":
            account.name = request.POST.get('account_name')
            account.value = request.POST.get('account_amount')
            category_id = request.POST.get('account_category')
            account.category = Category.objects.get(id=category_id)
            account.save()
            return redirect('account_plans')

def delete_account_plan(request, pk):
    if request.user.is_authenticated:
        delete_it = Account.objects.get(id=pk) #O método get() pega no banco de dados através do ID.
        delete_it.delete()
        messages.success(request, "Cadastro deletado com sucesso!")
        return redirect('accounts')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')