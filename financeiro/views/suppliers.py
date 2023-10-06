from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

def suppliers(request):
    if request.user.is_authenticated:
        supplier = Supplier.objects.all()
        return render(request, 'suppliers.html', {'suppliers': supplier})
    
def new_supplier(request):
    if request.user.is_authenticated:
        name = request.POST.get('name')
        supplier_type = request.POST.get('type')
        document = request.POST.get('document')
        phone = request.POST.get('telephone')
        email = request.POST.get('email')
        supplier = Supplier(name=name, document=document, type=supplier_type, telephone=phone, email=email)
        messages.success(request, "Cadastro realizado com sucesso!")
        supplier.save()
        return redirect('suppliers')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
def delete_supplier(request, pk):
    if request.user.is_authenticated:
        delete_it = Supplier.objects.get(id=pk) #O método get() pega no banco de dados através do ID.
        delete_it.delete()
        messages.success(request, "Cadastro deletado com sucesso!")
        return redirect('suppliers')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')