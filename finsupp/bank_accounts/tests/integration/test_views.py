import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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
class TestBankAccountViews:
    @pytest.mark.integration
    def test_home_exibe_link_para_contas(self, client, user):
        client.force_login(user)
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert reverse('bank_accounts:list') in response.content.decode()

    @pytest.mark.integration
    def test_lista_exige_login(self, client):
        response = client.get(reverse('bank_accounts:list'))
        assert response.status_code == 302

    @pytest.mark.integration
    def test_criar_conta_bancaria(self, client, user):
        client.force_login(user)
        data = {
            'name': 'Conta Nova',
            'institution': 'INTER',
            'account_type': 'CHECKING',
            'balance': '150.00',
            'closing_day': 10,
            'payment_due_day': 20,
            'cards-TOTAL_FORMS': '0',
            'cards-INITIAL_FORMS': '0',
            'cards-MIN_NUM_FORMS': '0',
            'cards-MAX_NUM_FORMS': '1000',
        }
        response = client.post(reverse('bank_accounts:create'), data)
        assert response.status_code == 302
        assert BankAccount.objects.filter(user=user, name='Conta Nova').exists()

    @pytest.mark.integration
    def test_editar_conta_bancaria(self, client, user):
        client.force_login(user)
        account = BankAccount.objects.create(
            user=user, 
            name='Conta Anterior', 
            institution='BB',
            closing_day=5,
            payment_due_day=10
        )
        data = {
            'name': 'Conta Editada',
            'institution': 'ITAU',
            'account_type': 'SAVINGS',
            'balance': '99.99',
            'closing_day': 1,
            'payment_due_day': 15,
            'cards-TOTAL_FORMS': '0',
            'cards-INITIAL_FORMS': '0',
            'cards-MIN_NUM_FORMS': '0',
            'cards-MAX_NUM_FORMS': '1000',
        }
        response = client.post(reverse('bank_accounts:update', args=[account.pk]), data)
        assert response.status_code == 302
        account.refresh_from_db()
        assert account.name == 'Conta Editada'
        assert account.institution == 'ITAU'
        assert account.account_type == 'SAVINGS'

    @pytest.mark.integration
    def test_excluir_conta_bancaria(self, client, user):
        client.force_login(user)
        account = BankAccount.objects.create(
            user=user, 
            name='Excluir', 
            closing_day=1, 
            payment_due_day=5
        )
        response = client.post(reverse('bank_accounts:delete', args=[account.pk]))
        assert response.status_code == 302
        assert not BankAccount.objects.filter(pk=account.pk).exists()

    @pytest.mark.integration
    def test_lista_mostra_apenas_contas_do_usuario_logado(self, client, user, other_user):
        client.force_login(user)
        BankAccount.objects.create(user=user, name='Minha Conta', closing_day=1, payment_due_day=1)
        BankAccount.objects.create(user=other_user, name='Conta Dele', closing_day=1, payment_due_day=1)

        response = client.get(reverse('bank_accounts:list'))

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Minha Conta' in content
        assert 'Conta Dele' not in content