from django import forms
from transactions.models import Transaction
from categories.models import Category
from bank_accounts.models import BankAccount

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['account'].queryset = BankAccount.objects.filter(user=self.user)
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
            
    class Meta:
        model = Transaction
        fields = ('description', 'amount', 'date', 'transaction_type', 'account', 'category')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Ex.: Compra no supermercado', 'autofocus': True}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
