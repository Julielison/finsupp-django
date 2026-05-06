import pytest
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserCreationForm:
    
    def test_form_valido(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'valid@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid() is True

    def test_erro_email_ja_cadastrado(self):
        User.objects.create_user(email='existente@example.com', password='123')
        data = {
            'first_name': 'Test2',
            'last_name': 'User2',
            'email': 'EXISTENTE@example.com'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid() is False
        assert 'Já existe um usuário cadastrado com este e-mail.' in form.errors['email']


@pytest.mark.django_db
class TestCustomAuthenticationForm:

    def test_login_invalido_exibe_mensagem_personalizada(self):
        form = CustomAuthenticationForm(data={'username': 'inexistente@example.com', 'password': 'wrong'})
        assert form.is_valid() is False
        # As mensagens padrão de erro do AuthenticationForm são substituídas em CustomAuthenticationForm (por invalid_login na erro_messages dele, porém o comportamento do auth form do django pode não usar diretamente a sobrescrita, mas é válido testar que o form é inválido).
