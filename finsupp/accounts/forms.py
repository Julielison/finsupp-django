from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('Nome'),
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': _('Seu nome'), 'autofocus': True}),
    )
    last_name = forms.CharField(
        label=_('Sobrenome'),
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': _('Seu sobrenome')}),
    )
    email = forms.EmailField(
        label=_('E-mail'),
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': _('seu@email.com')}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('Já existe um usuário cadastrado com este e-mail.'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('E-mail'),
        widget=forms.EmailInput(attrs={'placeholder': _('seu@email.com'), 'autofocus': True}),
    )

    error_messages = {
        'invalid_login': _('E-mail ou senha incorretos. Verifique suas credenciais e tente novamente.'),
        'inactive': _('Esta conta está inativa.'),
    }
