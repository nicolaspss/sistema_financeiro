from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

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
    transfers = Transfer.objects.all()
    accounts = Account.objects.all()
    bank_accounts = BankAccounts.objects.all()
    suppliers = Supplier.objects.all()
    sum_transfer=Transfer.objects.aggregate(Sum('value'))
    return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.warning(request, "Você foi desconectado.")
    return redirect('home')