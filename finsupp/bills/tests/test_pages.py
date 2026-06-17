from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import get_user_model
from ..models import Bill, BillItem


User = get_user_model()


class BillsPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@example.com', password='pass1234', first_name='T', last_name='U')
        self.client.force_login(self.user)
        from bank_accounts.models import BankAccount
        acct = BankAccount.objects.create(user=self.user, name='Conta Teste', balance=1000, closing_day=5, payment_due_day=10)
        self.bill = Bill.objects.create(account=acct, description='Conta A', total=100, due_date=timezone.now().date())
        BillItem.objects.create(bill=self.bill, description='Item 1', amount=100)

    def test_list_view_shows_bill(self):
        url = reverse('bills:list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Conta A')

    def test_detail_view_and_pay(self):
        url = reverse('bills:detail', args=[self.bill.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # pay the bill
        resp2 = self.client.post(url, {'pay': '1'}, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.status, Bill.Status.PAID)
