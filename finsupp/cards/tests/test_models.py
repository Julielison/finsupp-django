import pytest
from accounts.models import User
from bank_accounts.models import BankAccount
from cards.models import Card

@pytest.fixture
def user():
    return User.objects.create_user(
        email='test_card@example.com',
        password='password123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def bank_account(user):
    return BankAccount.objects.create(
        user=user,
        name='Main Account',
        institution='NUBANK',
        account_type='CHECKING',
        balance=1000.00,
        closing_day=5,
        payment_due_day=10
    )

@pytest.mark.django_db
class TestCardModel:
    def test_create_debit_card(self, bank_account):
        """Testa a criação de um cartão de débito simples."""
        card = Card.objects.create(
            description='My Debit Card',
            last_numbers='1234',
            limit=0,
            type=Card.CardType.DEBIT,
            account=bank_account
        )
        assert card.id is not None
        assert card.type == 'DEBIT'
        assert card.account == bank_account

    def test_create_credit_card(self, bank_account):
        """Testa a criação de um cartão de crédito com limite."""
        card = Card.objects.create(
            description='My Credit Card',
            last_numbers='5678',
            limit=5000,
            type=Card.CardType.CREDIT,
            account=bank_account
        )
        assert card.id is not None
        assert card.type == 'CREDIT'
        assert card.limit == 5000

    def test_create_both_card(self, bank_account):
        """Testa a criação de um cartão múltiplo (Crédito e Débito)."""
        card = Card.objects.create(
            description='My Multiple Card',
            last_numbers='9999',
            limit=10000,
            type=Card.CardType.BOTH,
            account=bank_account
        )
        assert card.id is not None
        assert card.type == 'BOTH'
        assert card.limit == 10000

    def test_card_str_representation(self, bank_account):
        """Testa o retorno do método __str__ do cartão."""
        card = Card.objects.create(
            description='Black Card',
            last_numbers='4321',
            limit=20000,
            type=Card.CardType.CREDIT,
            account=bank_account
        )
        assert str(card) == 'Black Card (4321)'
