from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    account = models.ForeignKey(
        'bank_accounts.BankAccount',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='conta bancária'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='categoria'
    )
    description = models.CharField('descrição', max_length=255)
    amount = models.DecimalField('valor', max_digits=12, decimal_places=2)
    date = models.DateField('data')
    transaction_type = models.CharField('tipo de transação', max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    card = models.ForeignKey(
        'cards.Card',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='cartão'
    )
    is_add_to_bill = models.BooleanField('adicionar na fatura', default=False)
    installments = models.IntegerField('parcelas', null=True, blank=True, default=1)
    
    class Meta:
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def clean(self):
        super().clean()
        if self.is_add_to_bill:
            if not self.card:
                raise ValidationError({"is_add_to_bill": "Um cartão deve ser informado para adicionar na fatura."})
            if self.card.type not in ['CREDIT', 'BOTH']:
                raise ValidationError({"is_add_to_bill": "Apenas transações com cartão de crédito podem ser adicionadas à fatura."})
