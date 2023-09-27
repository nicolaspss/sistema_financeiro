from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('contas/', views.accounts, name='accounts'),
    path('adicionar_contas/', views.add_account, name='add_account'),
    path('atualizar_contas/<int:pk>', views.update_account, name='update_account'),
    path('deletar_contas/<int:pk>', views.delete_account, name='delete_account'),
    path('contas/filtrar/', views.search_bar, name='search_bar'),

    path('plano_de_contas/', views.account_plans, name='account_plans'),
    path('adicionar_categoria/', views.add_new_category, name='add_new_category'),
    path('deletar_categoria/', views.delete_category, name='delete_category'),
    path('atualizar_categoria/', views.update_category, name='update_category'),
    path('adicionar_nova_conta/', views.add_new_account, name='add_new_account'),
    #path('atualizar_conta/<int:pk>', views.update_account_plan, name='update_account_plan'),
    #path('deletar_conta/<int:pk>', views.delete_account_plan, name='delete_account_plan'),

    path('fornecedores/', views.suppliers, name='suppliers'),
    path('adicionar_fornecedor/', views.new_supplier, name='new_supplier'),
    
    path('transferencias/', views.transfers, name='transfers'),
    path('deletar_transferencia/<int:pk>', views.delete_transfer, name='delete_transfer'),
    path('adicionar_recebimento/', views.add_new_receipt, name='new_receipt'),
    path('adicionar_pagamento/', views.add_new_payment, name='new_payment'),
    path('transferencias/filtrar/', views.filter_by_date, name='filtered_objects'),
]