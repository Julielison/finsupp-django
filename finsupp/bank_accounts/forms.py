from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from bank_accounts.models import BankAccount
from cards.models import Card

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
                    'placeholder': _('Ex.: Conta principal'),
                    'autofocus': True,
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 text-slate-900 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
                }
            ),
            'institution': forms.Select(
                attrs={
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
                }
            ),
            'account_type': forms.Select(
                attrs={
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
                }
            ),
            'balance': forms.NumberInput(
                attrs={
                    'placeholder': _('Ex: 1000'),
                    'step': '0.01',
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
                }
            ),
            'closing_day': forms.NumberInput(
                attrs={
                    'placeholder': _('Ex: 03'),
                    'min': '1',
                    'max': '31',
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
                }
            ),
            'payment_due_day': forms.NumberInput(
                attrs={
                    'placeholder': _('Ex: 10'),
                    'min': '1',
                    'max': '31',
                    'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500',
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
            raise ValidationError(_('Já existe uma conta bancária com este nome.'))

        return normalized_name

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('description', 'last_numbers', 'limit', 'type')
        widgets = {
            'description': forms.TextInput(attrs={'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500', 'placeholder': _('Ex: Nubank')}),
            'last_numbers': forms.TextInput(attrs={'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500', 'placeholder': _('Ex: 1234'), 'maxlength': '4'}),
            'limit': forms.NumberInput(attrs={'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500', 'placeholder': _('Ex: 5000'), 'step': '1'}),
            'type': forms.Select(attrs={'class': 'mt-2 block w-full rounded-xl border border-slate-300 px-3 py-2.5 shadow-sm focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500'}),
        }

CardFormSet = inlineformset_factory(BankAccount, Card, form=CardForm, extra=1, can_delete=True)