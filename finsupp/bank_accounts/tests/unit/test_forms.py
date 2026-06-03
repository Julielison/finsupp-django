import pytest
from django.contrib.auth import get_user_model

from bank_accounts.forms import BankAccountForm
from bank_accounts.models import BankAccount

User = get_user_model()


@pytest.mark.django_db
class TestBankAccountForm:
    @pytest.mark.unit
    def test_form_valido(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        data = {
            'name': 'Conta Corrente X',
            'institution': 'NUBANK',
            'account_type': 'CHECKING',
            'balance': '1000.50',
            'closing_day': 5,
            'payment_due_day': 10
        }
        form = BankAccountForm(user=user, data=data)
        assert form.is_valid() is True

    @pytest.mark.unit
    def test_form_ignora_espacos_no_name(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        data = {
            'name': '  Minha   Conta  ',
            'institution': 'ITAU',
            'account_type': 'SAVINGS',
            'balance': '0.00',
            'closing_day': 1,
            'payment_due_day': 1
        }
        form = BankAccountForm(user=user, data=data)
        assert form.is_valid() is True
        assert form.cleaned_data['name'] == 'Minha Conta'

    @pytest.mark.unit
    def test_form_bloqueia_duplicado(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        BankAccount.objects.create(
            user=user, 
            name='Conta Corrente',
            institution='BB',
            account_type='CHECKING',
            balance=100.00,
            closing_day=10,
            payment_due_day=15
        )
        data = {
            'name': 'CONTA CORRENTE',
            'institution': 'CAIXA',
            'account_type': 'SAVINGS',
            'balance': '0.00',
            'closing_day': 1,
            'payment_due_day': 1
        }
        form = BankAccountForm(user=user, data=data)
        assert form.is_valid() is False
        assert 'Já existe uma conta bancária com este nome.' in form.errors['name']

    @pytest.mark.unit
    def test_form_permite_mesmo_nome_para_usuario_diferente(self):
        user_one = User.objects.create_user(email='one@example.com', password='StrongPass123')
        user_two = User.objects.create_user(email='two@example.com', password='StrongPass123')
        BankAccount.objects.create(
            user=user_one, 
            name='Minha Conta',
            institution='BB',
            closing_day=10,
            payment_due_day=15
        )

        data = {
            'name': 'Minha Conta',
            'institution': 'BB',
            'account_type': 'CHECKING',
            'balance': '10.00',
            'closing_day': 5,
            'payment_due_day': 10
        }
        form = BankAccountForm(user=user_two, data=data)
        assert form.is_valid() is True

    @pytest.mark.unit
    def test_form_bloqueia_mesmo_nome_na_edicao_se_pertencer_a_outra_conta(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        BankAccount.objects.create(user=user, name='Conta A', closing_day=1, payment_due_day=10)
        conta_b = BankAccount.objects.create(user=user, name='Conta B', closing_day=1, payment_due_day=10)
        
        data = {
            'name': 'Conta A',
            'institution': 'BB',
            'account_type': 'CHECKING',
            'balance': '10.00',
            'closing_day': 5,
            'payment_due_day': 10
        }
        form = BankAccountForm(user=user, instance=conta_b, data=data)
        assert form.is_valid() is False
        assert 'Já existe uma conta bancária com este nome.' in form.errors['name']

    @pytest.mark.unit
    def test_form_dias_invalidos(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        data = {
            'name': 'Teste',
            'institution': 'BB',
            'account_type': 'CHECKING',
            'balance': '10.00',
            'closing_day': 32, # Invalido
            'payment_due_day': 0 # Invalido
        }
        form = BankAccountForm(user=user, data=data)
        assert form.is_valid() is False
        assert 'closing_day' in form.errors
        assert 'payment_due_day' in form.errors