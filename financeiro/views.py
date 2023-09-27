from django.shortcuts import render, redirect
from .models import BankAccounts, Category, Account, Transfer, Supplier
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
    return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.warning(request, "Você foi desconectado.")
    return redirect('home')

# Contas

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

# Barra de Pesquisa

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

# Plano de Contas

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
            amount = request.POST.get('account_amount')
            category_id = request.POST.get('account_category')
            category = Category.objects.get(id=category_id)
            account = Account(name=name, amount=amount, category=category)
            account.save()
            return redirect('account_plans')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')

def delete_account_plan(request, pk):
    if request.user.is_authenticated:
        delete_it = Account.objects.get(id=pk) #O método get() pega no banco de dados através do ID.
        delete_it.delete()
        messages.success(request, "Cadastro deletado com sucesso!")
        return redirect('accounts')
    else:
        messages.error(request, "Você deve estar logado para visualizar esta página.")
        return redirect('home')
    
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
    
def transfers(request):
    if request.user.is_authenticated:
        transfers = Transfer.objects.all().order_by('-id')
        accounts = Account.objects.all()
        bank_accounts = BankAccounts.objects.all()
        suppliers = Supplier.objects.all()
        sum_transfer=Transfer.objects.aggregate(Sum('value'))
        print(sum_transfer) 
        return render(request, 'transfers/transfers.html', {
            'transfers': transfers,
            'accounts': accounts,
            'bank_accounts': bank_accounts,
            'suppliers': suppliers,
            'transfer_sum': sum_transfer,
        })

def filter_by_date(request):
    if request.user.is_authenticated:
        start = request.GET.get('start')
        end = request.GET.get('end')
        transfers = Transfer.objects.filter(end_date__range=(start, end))
        return render(request, 'transfers/transfers_search.html', {'transfers': transfers})
    
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