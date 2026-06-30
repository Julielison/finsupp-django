from django.db import models

class Card(models.Model):
    class CardType(models.TextChoices):
        DEBIT = 'DEBIT', 'Débito'
        CREDIT = 'CREDIT', 'Crédito'
        BOTH = 'BOTH', 'Ambos'

    description = models.CharField('descrição', max_length=100)
    last_numbers = models.CharField('últimos números', max_length=4)
    limit = models.IntegerField('limite', default=0)
    type = models.CharField('tipo', max_length=10, choices=CardType.choices)
    account = models.ForeignKey(
        'bank_accounts.BankAccount',
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='conta bancária'
    )

    class Meta:
        verbose_name = 'cartão'
        verbose_name_plural = 'cartões'

    def __str__(self):
        return f"{self.description} ({self.last_numbers})"
