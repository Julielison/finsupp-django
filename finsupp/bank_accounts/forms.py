from django import forms
from django.core.exceptions import ValidationError

from bank_accounts.models import BankAccount

class BankAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = BankAccount
        fields = ('name', 'balance', 'institution')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: Nubank',
                    'autofocus': True,
                }
            ),
            'balance': forms.NumberInput(
                attrs={
                    'placeholder': 'Ex.: 1000.00',
                    'step': '0.01',
                }
            ),
            'institution': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: Banco Nubank SA',
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