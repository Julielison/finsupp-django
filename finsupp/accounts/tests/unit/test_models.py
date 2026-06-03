import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    
    @pytest.mark.unit
    def test_criar_usuario_com_dados_validos(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        
    @pytest.mark.unit
    def test_criar_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            first_name='Admin',
            last_name='Super'
        )
        assert admin.email == 'admin@example.com'
        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True

    @pytest.mark.unit
    def test_senha_armazenada_com_hash(self):
        user = User.objects.create_user(
            email='hash@example.com',
            password='mysecretpassword'
        )
        assert getattr(user, 'password') != 'mysecretpassword'
        assert user.check_password('mysecretpassword') is True

    @pytest.mark.unit
    def test_email_deve_ser_unico(self):
        User.objects.create_user(email='unique@example.com', password='123')
        with pytest.raises(IntegrityError):
            User.objects.create_user(email='unique@example.com', password='456')

    @pytest.mark.unit
    def test_string_representation(self):
        user1 = User.objects.create_user(email='full@example.com', password='123', first_name='John', last_name='Doe')
        assert str(user1) == 'John Doe'
        
        user2 = User.objects.create_user(email='nofull@example.com', password='123')
        assert str(user2) == 'nofull@example.com'
        
    @pytest.mark.unit
    def test_get_short_name(self):
        user = User.objects.create_user(email='short@example.com', password='123', first_name='John')
        assert user.get_short_name() == 'John'
