from django.urls import path

from bank_accounts.views import (
    BankAccountCreateView,
    BankAccountDeleteView,
    BankAccountListView,
    BankAccountUpdateView,
)

app_name = 'bank_accounts'

urlpatterns = [
    path('', BankAccountListView.as_view(), name='list'),
    path('nova/', BankAccountCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', BankAccountUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', BankAccountDeleteView.as_view(), name='delete'),
]