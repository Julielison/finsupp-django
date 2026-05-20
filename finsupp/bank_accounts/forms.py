from django import forms
from django.core.exceptions import ValidationError

from bank_accounts.models import BankAccount

class BankAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = BankAccount
        fields = ('name', 'institution', 'account_type', 'balance', 'closing_day', 'payment_due_day')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: Conta principal',
                    'autofocus': True,
                }
            ),
            'institution': forms.Select(
                attrs={
                    'class': 'mt-2 block w-full rounded-xl border border-input bg-background px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
                }
            ),
            'account_type': forms.Select(
                attrs={
                    'class': 'mt-2 block w-full rounded-xl border border-input bg-background px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
                }
            ),
            'balance': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 1000',
                    'step': '0.01',
                }
            ),
            'closing_day': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 03',
                    'min': '1',
                    'max': '31'
                }
            ),
            'payment_due_day': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex: 10',
                    'min': '1',
                    'max': '31'
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        normalized_name = ' '.join(name.split()).strip()

        existing_accounts = BankAccount.objects.filter(name__iexact=normalized_name)

        if self.user is not None:
            existing_accounts = existing_accounts.filter(user=self.user)

        if self.instance and self.instance.pk:
            existing_accounts = existing_accounts.exclude(pk=self.instance.pk)

        if existing_accounts.exists():
            raise ValidationError('Já existe uma conta bancária com este nome.')

        return normalized_name