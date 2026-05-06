import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()

@pytest.mark.django_db
class TestAuthViews:

    def test_registro_sucesso(self, client):
        url = reverse('accounts:signup')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        }
        response = client.post(url, data)
        # Assumindo onSuccess redirect para login
        assert response.status_code in [200, 302]
        if response.status_code == 302:
            assert response.url == reverse('accounts:login')
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_registro_email_duplicado(self, client):
        User.objects.create_user(email='duplicado@example.com', password='123')
        url = reverse('accounts:signup')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'duplicado@example.com'
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert not response.context['form'].is_valid()
        assert 'Já existe um usuário cadastrado com este e-mail.' in response.context['form'].errors['email']

    def test_login_sucesso(self, client):
        User.objects.create_user(email='login@example.com', password='validpassword123')
        url = reverse('accounts:login')
        data = {
            'username': 'login@example.com',
            'password': 'validpassword123'
        }
        response = client.post(url, data)
        assert str(response.url).startswith('/')  # Redirects to home or specific URL

    def test_login_credenciais_invalidas(self, client):
        User.objects.create_user(email='login@example.com', password='validpassword123')
        url = reverse('accounts:login')
        data = {
            'username': 'login@example.com',
            'password': 'wrongpassword'
        }
        response = client.post(url, data)
        assert response.status_code == 200
        assert not response.context['form'].is_valid()

    def test_logout(self, client):
        user = User.objects.create_user(email='logout@example.com', password='123')
        client.force_login(user)
        url = reverse('accounts:logout')
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('accounts:login')

    def test_password_reset_email_existente(self, client):
        User.objects.create_user(email='reset@example.com', password='123')
        url = reverse('accounts:password_reset')
        data = {'email': 'reset@example.com'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('accounts:password_reset_done')
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ['reset@example.com']

    def test_password_reset_email_inexistente(self, client):
        # Mesmo se o e-mail não existir, o comportamento padrão não levanta exceção prevendo enumeração
        url = reverse('accounts:password_reset')
        data = {'email': 'inexistente@example.com'}
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('accounts:password_reset_done')
        assert len(mail.outbox) == 0
