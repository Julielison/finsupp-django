from django.db import models
from django.utils.translation import gettext_lazy as _

class Card(models.Model):
    class CardType(models.TextChoices):
        DEBIT = 'DEBIT', _('Débito')
        CREDIT = 'CREDIT', _('Crédito')
        BOTH = 'BOTH', _('Ambos')

    description = models.CharField(_('descrição'), max_length=100)
    last_numbers = models.CharField(_('últimos números'), max_length=4)
    limit = models.IntegerField(_('limite'), default=0)
    type = models.CharField(_('tipo'), max_length=10, choices=CardType.choices)
    account = models.ForeignKey(
        'bank_accounts.BankAccount',
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name=_('conta bancária')
    )

    class Meta:
        verbose_name = _('cartão')
        verbose_name_plural = _('cartões')

    def __str__(self):
        return f"{self.description} ({self.last_numbers})"
