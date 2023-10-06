from django.shortcuts import render, redirect
from financeiro.models import BankAccounts, Category, Account, Transfer, Supplier
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count, Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.template.loader import get_template
from xhtml2pdf import pisa

def reports(request):
    return render(request, 'reports/reports.html', {})

def generate_pdf(request):
    # Get your HTML content here, or render it from a template
    template = get_template('reports/pdf_template.html')
    transfers = Transfer.objects.all().order_by('-start_date').reverse()
    accounts = Account.objects.all()
    bank_accounts = BankAccounts.objects.all()
    suppliers = Supplier.objects.all()
    sum_transfer=Transfer.objects.aggregate(Sum('value'))
    context = {
            'transfers': transfers,
            'accounts': accounts,
            'bank_accounts': bank_accounts,
            'suppliers': suppliers,
            'transfer_sum': sum_transfer,
        }  # Optional: Provide context data

    html_content = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'

    # Generate the PDF from HTML
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Check if PDF generation was successful
    if pisa_status.err: # type: ignore
        return HttpResponse('PDF generation error', content_type='text/plain')
    return response