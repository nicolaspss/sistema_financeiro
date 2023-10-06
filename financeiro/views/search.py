from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

def search_bar(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        if searched:
            account_query = BankAccounts.objects.filter(
                Q(name__contains=searched)|Q(account_type__icontains=searched)|Q(account_number__icontains=searched)
            ).values()
            return render(request, 'accounts/account_search.html', {'searched': searched, 'account_query': account_query,})
        else:
            return redirect('accounts')