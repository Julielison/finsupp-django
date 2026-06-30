from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('INCOME', _('Receita')),
        ('EXPENSE', _('Despesa')),
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
        verbose_name=_('conta bancária')
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name=_('categoria')
    )
    description = models.CharField(_('descrição'), max_length=255)
    amount = models.DecimalField(_('valor'), max_digits=12, decimal_places=2)
    date = models.DateField(_('data'))
    transaction_type = models.CharField(_('tipo de transação'), max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    card = models.ForeignKey(
        'cards.Card',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name=_('cartão')
    )
    is_add_to_bill = models.BooleanField(_('adicionar na fatura'), default=False)
    installments = models.IntegerField(_('parcelas'), null=True, blank=True, default=1)
    
    class Meta:
        verbose_name = _('transação')
        verbose_name_plural = _('transações')
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.description} - {self.amount}"

    def clean(self):
        super().clean()
        if self.is_add_to_bill:
            if not self.card:
                raise ValidationError({"is_add_to_bill": _("Um cartão deve ser informado para adicionar na fatura.")})
            if self.card.type not in ['CREDIT', 'BOTH']:
                raise ValidationError({"is_add_to_bill": _("Apenas transações com cartão de crédito podem ser adicionadas à fatura.")})
