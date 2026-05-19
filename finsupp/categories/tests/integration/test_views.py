import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from categories.models import Category

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        first_name='Teste',
        last_name='Usuario',
        email='teste@example.com',
        password='StrongPass123',
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        first_name='Outro',
        last_name='Usuario',
        email='outro@example.com',
        password='StrongPass123',
    )


@pytest.mark.django_db
class TestCategoryViews:
    def test_home_exibe_link_para_categorias(self, client, user):
        client.force_login(user)
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert reverse('categories:list') in response.content.decode()

    def test_lista_exige_login(self, client):
        response = client.get(reverse('categories:list'))
        assert response.status_code == 302

    def test_criar_categoria(self, client, user):
        client.force_login(user)
        response = client.post(reverse('categories:create'), {'description': 'alimentação'})
        assert response.status_code == 302
        assert Category.objects.filter(user=user, description='Alimentação').exists()

    def test_editar_categoria(self, client, user):
        client.force_login(user)
        category = Category.objects.create(user=user, description='Transporte')
        response = client.post(reverse('categories:update', args=[category.pk]), {'description': 'Mobilidade'})
        assert response.status_code == 302
        category.refresh_from_db()
        assert category.description == 'Mobilidade'

    def test_excluir_categoria(self, client, user):
        client.force_login(user)
        category = Category.objects.create(user=user, description='Lazer')
        response = client.post(reverse('categories:delete', args=[category.pk]))
        assert response.status_code == 302
        assert not Category.objects.filter(pk=category.pk).exists()

    def test_lista_mostra_apenas_categorias_do_usuario_logado(self, client, user, other_user):
        client.force_login(user)
        Category.objects.create(user=user, description='Casa')
        Category.objects.create(user=other_user, description='Trabalho')

        response = client.get(reverse('categories:list'))

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Casa' in content
        assert 'Trabalho' not in content