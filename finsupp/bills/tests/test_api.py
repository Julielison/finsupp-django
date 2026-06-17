from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from bank_accounts.models import BankAccount as Account
from ..models import Bill, BillItem

User = get_user_model()


class BillApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@u.com', password='pw', first_name='U', last_name='X')
        self.other = User.objects.create_user(email='o@o.com', password='pw', first_name='O', last_name='X')
        self.account = Account.objects.create(user=self.user, name='acc', balance=1000, institution='ITAU', closing_day=1, payment_due_day=5)
        self.other_account = Account.objects.create(user=self.other, name='acc2', balance=500, institution='ITAU', closing_day=1, payment_due_day=5)
        self.bill = Bill.objects.create(account=self.account, total=100, due_date='2026-06-20')

    def test_list_bills_authenticated(self):
        self.client.force_login(self.user)
        url = reverse('bill-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.data) >= 1)

    def test_pay_bill_conflict_if_already_paid(self):
        self.client.force_login(self.user)
        self.bill.status = Bill.Status.PAID
        self.bill.save()
        url = reverse('bill-pay', args=[self.bill.id])
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, 409)

    def test_pay_bill_forbidden_for_other_user(self):
        self.client.force_login(self.other)
        url = reverse('bill-pay', args=[self.bill.id])
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, 404)

    def test_create_bill_with_items_via_api(self):
        self.client.force_login(self.user)
        url = reverse('bill-list')
        payload = {
            'account': self.account.id,
            'total': '150.00',
            'due_date': '2026-07-01',
            'items': [
                {'description': 'it1', 'amount': '150.00'}
            ]
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
