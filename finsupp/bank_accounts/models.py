from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class BankAccount(models.Model):
    BANK_CHOICES = [
        ('BB', 'Banco do Brasil'),
        ('CAIXA', 'Caixa Econômica Federal'),
        ('BRADESCO', 'Bradesco'),
        ('ITAU', 'Itaú'),
        ('SANTANDER', 'Santander'),
        ('NUBANK', 'Nubank'),
        ('INTER', 'Inter'),
        ('BTG', 'BTG Pactual'),
        ('C6', 'C6 Bank'),
        ('OUTRO', 'Outro'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('CHECKING', 'Conta Corrente'),
        ('SAVINGS', 'Conta Poupança'),
        ('INVESTMENT', 'Investimento'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    name = models.CharField('descrição', max_length=100)
    institution = models.CharField('banco', max_length=20, choices=BANK_CHOICES, blank=True, null=True)
    account_type = models.CharField('tipo da conta', max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='CHECKING')
    balance = models.DecimalField('saldo', max_digits=12, decimal_places=2, default=0.00)
    closing_day = models.IntegerField('dia de fechamento', validators=[MinValueValidator(1), MaxValueValidator(31)])
    payment_due_day = models.IntegerField('dia de vencimento (pagamento)', validators=[MinValueValidator(1), MaxValueValidator(31)])

    class Meta:
        verbose_name = 'conta bancária'
        verbose_name_plural = 'contas bancárias'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_bank_account_per_user'),
        ]

    def __str__(self):
        return self.name