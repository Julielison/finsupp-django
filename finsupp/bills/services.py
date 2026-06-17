from datetime import date
from django.db import transaction
from .models import Bill, BillItem
try:
    from transactions.services import TransactionService
except Exception:
    TransactionService = None

from .exceptions import BillAlreadyPaid, BillPaymentError


class BillService:
    @staticmethod
    def pay_bill(bill: Bill, paid_by_user, payment_account=None):
        if bill.status == Bill.Status.PAID:
            raise BillAlreadyPaid("Bill already paid")
        # create a transaction to debit account via TransactionService
        try:
            with transaction.atomic():
                tx = None
                if TransactionService is not None:
                    tx = TransactionService.create_payment(
                        account=bill.account,
                        amount=bill.total,
                        description=f"Payment for bill {bill.id}",
                        performed_by=paid_by_user,
                    )
                else:
                    # best-effort: decrement account.balance if model has balance field
                    try:
                        acct = bill.account
                        if hasattr(acct, 'balance'):
                            acct.balance = acct.balance - bill.total
                            acct.save()
                    except Exception:
                        pass
                # link bill items to transaction when available
                bill.status = Bill.Status.PAID
                bill.paid_date = date.today()
                bill.save()
                if tx is not None:
                    for item in bill.items.all():
                        try:
                            item.transaction = tx
                            item.save()
                        except Exception:
                            # non-fatal linking error
                            pass
                return tx
        except Exception as exc:
            raise BillPaymentError(str(exc))

    @staticmethod
    def generate_bills_for_date(target_date: date):
        try:
            from subscriptions.models import Subscription
        except Exception:
            return []

        subs = Subscription.objects.filter(active=True)
        created = []
        for s in subs:
            due = None
            if hasattr(s, 'next_due_date'):
                due = s.next_due_date()
            if due == target_date:
                bill = Bill.objects.create(
                    account=s.account,
                    total=s.amount,
                    due_date=due,
                    description=f"Subscription {s.id}"
                )
                BillItem.objects.create(
                    bill=bill, description=s.description or f"Subscription {s.id}", amount=s.amount, subscription_id=s.id
                )
                created.append(bill)
        return created
