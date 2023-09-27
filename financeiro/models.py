from django.db import models

class BankAccounts(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ("Corrente", "Corrente"),
        ("Poupança", "Poupança")
    )

    name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    account_number = models.CharField(max_length=12)
    agency = models.IntegerField(null=True, blank=True)
    titular_name = models.CharField(max_length=50)
    titular_document = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=32)
    value = models.FloatField(null=True)
    category = models.ForeignKey(Category, models.CASCADE)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.name

class Supplier(models.Model):
    TYPE_CHOICES = (
        ("Física", "Física"),
        ("Jurídica", "Juridica")
    )

    name = models.CharField(max_length=64)
    document = models.IntegerField(blank=True)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, blank=True)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Transfer(models.Model):
    TRANSFER_CHOICES = (
        ("Recebimento", "Recebimento"),
        ("Pagamento", "Pagamento"),
        ("Transferência","Transferência")
    )

    name = models.CharField(max_length=32, blank=True, null=True)
    value = models.FloatField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, models.CASCADE)
    transfer_type = models.CharField(max_length=13, choices=TRANSFER_CHOICES)
    account = models.ForeignKey(Account, models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    bank_account = models.ForeignKey(BankAccounts, models.CASCADE)