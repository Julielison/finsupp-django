import pytest
from django.core.exceptions import ValidationError
from datetime import date
from transactions.models import Transaction
from cards.models import Card
from bank_accounts.models import BankAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(email='test@example.com', password='testpassword')

@pytest.fixture
def account(db, user):
    return BankAccount.objects.create(
        user=user,
        name='Test Account',
        account_type='CHECKING',
        closing_day=1,
        payment_due_day=10
    )

@pytest.fixture
def debit_card(db, account):
    return Card.objects.create(
        description='Debit Card',
        last_numbers='1234',
        type='DEBIT',
        account=account
    )

@pytest.fixture
def credit_card(db, account):
    return Card.objects.create(
        description='Credit Card',
        last_numbers='5678',
        limit=1000,
        type='CREDIT',
        account=account
    )
@pytest.fixture
def both_card(db, account):
    return Card.objects.create(
        description='Multiple Card',
        last_numbers='9999',
        limit=2000,
        type='BOTH',
        account=account
    )
@pytest.mark.django_db
@pytest.mark.unit
class TestTransactionModel:
    
    def test_transaction_add_to_bill_with_debit_card_raises_error(self, user, account, debit_card):
        transaction = Transaction(
            user=user,
            account=account,
            description='Test Debit',
            amount=100.0,
            date=date.today(),
            transaction_type='EXPENSE',
            card=debit_card,
            is_add_to_bill=True
        )
        
        with pytest.raises(ValidationError) as excinfo:
            transaction.clean()
        
        assert 'is_add_to_bill' in excinfo.value.error_dict
        assert 'Apenas transações com cartão de crédito podem ser adicionadas à fatura' in str(excinfo.value.error_dict['is_add_to_bill'][0])

    def test_transaction_add_to_bill_with_no_card_raises_error(self, user, account):
        transaction = Transaction(
            user=user,
            account=account,
            description='Test No Card',
            amount=100.0,
            date=date.today(),
            transaction_type='EXPENSE',
            is_add_to_bill=True
        )
        
        with pytest.raises(ValidationError) as excinfo:
            transaction.clean()
            
        assert 'is_add_to_bill' in excinfo.value.error_dict
        assert 'Um cartão deve ser informado' in str(excinfo.value.error_dict['is_add_to_bill'][0])

    def test_transaction_add_to_bill_with_credit_card_is_valid(self, user, account, credit_card):
        transaction = Transaction(
            user=user,
            account=account,
            description='Test Credit',
            amount=100.0,
            date=date.today(),
            transaction_type='EXPENSE',
            card=credit_card,
            is_add_to_bill=True
        )
        
        # Should not raise exception
        transaction.clean()
        assert transaction.is_add_to_bill is True
    def test_transaction_add_to_bill_with_both_card_is_valid(self, user, account, both_card):
        transaction = Transaction(
            user=user,
            account=account,
            description='Test Both',
            amount=100.0,
            date=date.today(),
            transaction_type='EXPENSE',
            card=both_card,
            is_add_to_bill=True
        )
        
        # Should not raise exception
        transaction.clean()
        assert transaction.is_add_to_bill is True
