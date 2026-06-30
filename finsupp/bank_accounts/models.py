from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class BankAccount(models.Model):
    BANK_CHOICES = [
        ('BB', _('Banco do Brasil')),
        ('CAIXA', _('Caixa Econômica Federal')),
        ('BRADESCO', _('Bradesco')),
        ('ITAU', _('Itaú')),
        ('SANTANDER', _('Santander')),
        ('NUBANK', _('Nubank')),
        ('INTER', _('Inter')),
        ('BTG', _('BTG Pactual')),
        ('C6', _('C6 Bank')),
        ('OUTRO', _('Outro')),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('CHECKING', _('Conta Corrente')),
        ('SAVINGS', _('Conta Poupança')),
        ('INVESTMENT', _('Investimento')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    name = models.CharField(_('descrição'), max_length=100)
    institution = models.CharField(_('banco'), max_length=20, choices=BANK_CHOICES, blank=True, null=True)
    account_type = models.CharField(_('tipo da conta'), max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='CHECKING')
    balance = models.DecimalField(_('saldo'), max_digits=12, decimal_places=2, default=0.00)
    closing_day = models.IntegerField(_('dia de fechamento'), validators=[MinValueValidator(1), MaxValueValidator(31)])
    payment_due_day = models.IntegerField(_('dia de vencimento (pagamento)'), validators=[MinValueValidator(1), MaxValueValidator(31)])

    class Meta:
        verbose_name = _('conta bancária')
        verbose_name_plural = _('contas bancárias')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_bank_account_per_user'),
        ]

    def __str__(self):
        return self.name