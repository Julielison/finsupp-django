import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal
import datetime

from transactions.forms import TransactionForm
from categories.models import Category
from bank_accounts.models import BankAccount

User = get_user_model()

@pytest.mark.django_db
class TestTransactionForm:
    def test_form_valido(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        category = Category.objects.create(user=user, description='Alimentação')
        account = BankAccount.objects.create(user=user, name='Conta', closing_day=1, payment_due_day=5)
        
        data = {
            'description': 'Compra',
            'amount': '150.50',
            'date': datetime.date.today().isoformat(),
            'transaction_type': 'EXPENSE',
            'account': account.pk,
            'category': category.pk
        }
        form = TransactionForm(user=user, data=data)
        assert form.is_valid() is True

    def test_form_apenas_contas_categorias_do_usuario(self):
        user1 = User.objects.create_user(email='user1@example.com', password='StrongPass123')
        user2 = User.objects.create_user(email='user2@example.com', password='StrongPass123')
        
        cat2 = Category.objects.create(user=user2, description='Lazer')
        acc2 = BankAccount.objects.create(user=user2, name='Conta 2', closing_day=1, payment_due_day=5)
        
        form = TransactionForm(user=user1)
        assert cat2 not in form.fields['category'].queryset
        assert acc2 not in form.fields['account'].queryset
