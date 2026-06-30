from django import forms
from django.utils.translation import gettext_lazy as _
from transactions.models import Transaction
from categories.models import Category
from bank_accounts.models import BankAccount
from cards.models import Card

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['account'].queryset = BankAccount.objects.filter(user=self.user)
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
            self.fields['card'].queryset = Card.objects.filter(account__user=self.user)
            
    class Meta:
        model = Transaction
        fields = ('description', 'amount', 'date', 'transaction_type', 'account', 'category', 'card', 'is_add_to_bill', 'installments')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': _('Ex.: Compra no supermercado'), 'autofocus': True}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        card = cleaned_data.get('card')
        is_add_to_bill = cleaned_data.get('is_add_to_bill')
        
        if is_add_to_bill:
            if not card:
                self.add_error('is_add_to_bill', _('Um cartão deve ser informado para adicionar na fatura.'))
            elif card.type not in ['CREDIT', 'BOTH']:
                self.add_error('is_add_to_bill', _('Apenas transações com cartão de crédito podem ser adicionadas à fatura.'))
                
        return cleaned_data
