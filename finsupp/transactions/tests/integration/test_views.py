import pytest
import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse

from transactions.models import Transaction
from categories.models import Category
from bank_accounts.models import BankAccount

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        first_name='Teste',
        last_name='Usuario',
        email='teste@example.com',
        password='StrongPass123',
    )

@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        first_name='Outro',
        last_name='Usuario',
        email='outro@example.com',
        password='StrongPass123',
    )

@pytest.mark.django_db
class TestTransactionViews:
    @pytest.mark.integration
    def test_home_exibe_link_para_transacoes(self, client, user):
        client.force_login(user)
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert reverse('transactions:list') in response.content.decode()

    @pytest.mark.integration
    def test_lista_exige_login(self, client):
        response = client.get(reverse('transactions:list'))
        assert response.status_code == 302

    @pytest.mark.integration
    def test_criar_transacao(self, client, user):
        client.force_login(user)
        category = Category.objects.create(user=user, description='Mercado')
        account = BankAccount.objects.create(user=user, name='Corrente', closing_day=1, payment_due_day=5)
        
        response = client.post(reverse('transactions:create'), {
            'description': 'Compra',
            'amount': '150.50',
            'date': datetime.date.today().isoformat(),
            'transaction_type': 'EXPENSE',
            'category': category.pk,
            'account': account.pk,
        })
        
        assert response.status_code == 302
        assert Transaction.objects.filter(user=user, description='Compra').exists()

    @pytest.mark.integration
    def test_editar_transacao(self, client, user):
        client.force_login(user)
        account = BankAccount.objects.create(user=user, name='Corrente', closing_day=1, payment_due_day=5)
        transaction = Transaction.objects.create(
            user=user, description='Compra Antiga', amount='100.00', 
            date=datetime.date.today(), transaction_type='EXPENSE', account=account
        )
        
        response = client.post(reverse('transactions:update', args=[transaction.pk]), {
            'description': 'Compra Nova',
            'amount': '120.00',
            'date': datetime.date.today().isoformat(),
            'transaction_type': 'EXPENSE',
            'account': account.pk
        })
        
        assert response.status_code == 302
        transaction.refresh_from_db()
        assert transaction.description == 'Compra Nova'
        assert transaction.amount == 120.00

    @pytest.mark.integration
    def test_excluir_transacao(self, client, user):
        client.force_login(user)
        account = BankAccount.objects.create(user=user, name='Corrente', closing_day=1, payment_due_day=5)
        transaction = Transaction.objects.create(
            user=user, description='Compra a cancelar', amount='100.00', 
            date=datetime.date.today(), transaction_type='EXPENSE', account=account
        )
        
        response = client.post(reverse('transactions:delete', args=[transaction.pk]))
        assert response.status_code == 302
        assert not Transaction.objects.filter(pk=transaction.pk).exists()

    @pytest.mark.integration
    def test_lista_mostra_apenas_transacoes_do_usuario_logado(self, client, user, other_user):
        client.force_login(user)
        account = BankAccount.objects.create(user=user, name='Corrente', closing_day=1, payment_due_day=5)
        Transaction.objects.create(
            user=user, description='Minha Transacao', amount='10.00', 
            date=datetime.date.today(), transaction_type='INCOME', account=account
        )
        
        account_other = BankAccount.objects.create(user=other_user, name='Outra', closing_day=1, payment_due_day=5)
        Transaction.objects.create(
            user=other_user, description='Transacao Dele', amount='50.00', 
            date=datetime.date.today(), transaction_type='EXPENSE', account=account_other
        )

        response = client.get(reverse('transactions:list'))

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Minha Transacao' in content
        assert 'Transacao Dele' not in content
