from django.contrib import admin
from .models import BankAccounts, Account, Category, Transfer, Supplier

admin.site.register(BankAccounts)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transfer)
admin.site.register(Supplier)