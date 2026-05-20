from django.conf import settings
from django.db import models

class BankAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )
    name = models.CharField('nome', max_length=100)
    balance = models.DecimalField('saldo', max_digits=12, decimal_places=2, default=0.00)
    institution = models.CharField('instituição', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'conta bancária'
        verbose_name_plural = 'contas bancárias'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_bank_account_per_user'),
        ]

    def __str__(self):
        return self.name