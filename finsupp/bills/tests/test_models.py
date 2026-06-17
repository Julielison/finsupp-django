from django.test import TestCase
from django.contrib.auth import get_user_model
from bank_accounts.models import BankAccount as Account
from ..models import Bill, BillItem

User = get_user_model()


class BillModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@u.com', password='pw', first_name='U', last_name='X')
        self.account = Account.objects.create(user=self.user, name='acc', balance=1000, institution='ITAU', closing_day=1, payment_due_day=5)

    def test_create_bill_with_items(self):
        bill = Bill.objects.create(account=self.account, total=100, due_date='2026-06-20')
        item = BillItem.objects.create(bill=bill, description='item1', amount=100)
        self.assertEqual(bill.items.count(), 1)

    def test_pay_bill_changes_status(self):
        bill = Bill.objects.create(account=self.account, total=50, due_date='2026-06-20')
        bill.pay()
        self.assertEqual(bill.status, Bill.Status.PAID)
