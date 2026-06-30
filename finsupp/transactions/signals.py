from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from datetime import date
from decimal import Decimal
import calendar
from transactions.models import Transaction
from bills.models import Bill, BillItem

def safe_date(year, month, day):
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, last_day))

def get_due_date_for_cycle(tx_date, closing_day, due_day):
    # Encontra a qual ciclo a transação pertence baseando-se no dia de fechamento
    closing_this_month = safe_date(tx_date.year, tx_date.month, closing_day)
    
    if tx_date <= closing_this_month:
        target_closing = closing_this_month
    else:
        next_month = tx_date + relativedelta(months=1)
        target_closing = safe_date(next_month.year, next_month.month, closing_day)
        
    # Calcula o dia de vencimento com base na data de fechamento determinada acima
    due_this_month = safe_date(target_closing.year, target_closing.month, due_day)
    if due_this_month >= target_closing:
        due_date = due_this_month
    else:
        next_due_month = target_closing + relativedelta(months=1)
        due_date = safe_date(next_due_month.year, next_due_month.month, due_day)
        
    return due_date

def process_transaction_bills(transaction):
    existing_items = list(BillItem.objects.filter(transaction=transaction))
    
    # Se a transação deixou de qualificar para fatura (foi desmarcada ou mudou cartão para Débito)
    if not transaction.is_add_to_bill or not transaction.card or transaction.card.type not in ['CREDIT', 'BOTH']:
        for item in existing_items:
            if item.bill.status == Bill.Status.OPEN:
                bill = item.bill
                item.delete()
                update_or_delete_bill(bill)
        return

    installments = transaction.installments or 1
    if installments < 1:
        installments = 1
        
    closed_items = [item for item in existing_items if item.bill.status != Bill.Status.OPEN]
    open_items = [item for item in existing_items if item.bill.status == Bill.Status.OPEN]
    
    # Deleta as parcelas abertas para recriá-las com valores atualizados
    for item in open_items:
        bill = item.bill
        item.delete()
        update_or_delete_bill(bill)
        
    closing_day = transaction.account.closing_day
    due_day = transaction.account.payment_due_day
    
    amount_per_installment = Decimal(transaction.amount) / Decimal(installments)
    amount_per_installment = amount_per_installment.quantize(Decimal('0.01'))
    
    for i in range(installments):
        current_tx_date = transaction.date + relativedelta(months=i)
        due_date = get_due_date_for_cycle(current_tx_date, closing_day, due_day)
        
        # Pula as faturas que já foram fechadas
        has_closed = any(item.bill.due_date == due_date for item in closed_items)
        if has_closed:
            continue
            
        amount = amount_per_installment
        if i == 0:
            # Corrige centavos que sobram/faltam por conta de divisões (ex: 100/3 = 33.33 -> falta 0.01)
            amount += Decimal(transaction.amount) - (amount_per_installment * Decimal(installments))
            
        bill, created = Bill.objects.get_or_create(
            account=transaction.account,
            due_date=due_date,
            status=Bill.Status.OPEN,
            defaults={'total': 0, 'description': f"Fatura {due_date.strftime('%m/%Y')}"}
        )
        
        desc = transaction.description
        if installments > 1:
            desc += f" ({i+1}/{installments})"
            
        BillItem.objects.create(
            bill=bill,
            transaction=transaction,
            description=desc,
            amount=amount
        )
        
        update_or_delete_bill(bill)

def update_or_delete_bill(bill):
    # Calcula o novo total e apaga a fatura se ficar vazia
    total = bill.items.aggregate(Sum('amount'))['amount__sum'] or 0
    if total <= 0:
        if bill.status == Bill.Status.OPEN:
            bill.delete()
    else:
        bill.total = total
        bill.save()

@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, **kwargs):
    process_transaction_bills(instance)

@receiver(post_delete, sender=Transaction)
def transaction_post_delete(sender, instance, **kwargs):
    items = list(BillItem.objects.filter(transaction=instance))
    for item in items:
        if item.bill.status == Bill.Status.OPEN:
            bill = item.bill
            item.delete()
            update_or_delete_bill(bill)
