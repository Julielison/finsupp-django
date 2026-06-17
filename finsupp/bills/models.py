from django.db import models
from django.conf import settings
from django.utils import timezone

from bank_accounts.models import BankAccount as Account
from transactions.models import Transaction


class Bill(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN"
        PAID = "PAID"
        CANCELED = "CANCELED"

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="bills")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def pay(self, paid_by=None, payment_transaction: Transaction = None):
        if self.status == self.Status.PAID:
            raise ValueError("Bill already paid")
        # If payment_transaction provided, link items accordingly handled elsewhere
        self.status = self.Status.PAID
        self.paid_date = timezone.now().date()
        self.save()


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
