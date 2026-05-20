import pytest
from django.contrib.auth import get_user_model

from categories.forms import CategoryForm
from categories.models import Category

User = get_user_model()


@pytest.mark.django_db
class TestCategoryForm:
    def test_form_valido(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        form = CategoryForm(user=user, data={'description': 'alimentação'})
        assert form.is_valid() is True

    def test_form_normaliza_descricao(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        form = CategoryForm(user=user, data={'description': '  agua e luz  '})
        assert form.is_valid() is True
        assert form.cleaned_data['description'] == 'Agua E Luz'

    def test_form_bloqueia_duplicado(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        Category.objects.create(user=user, description='Alimentação')
        form = CategoryForm(user=user, data={'description': 'ALIMENTAÇÃO'})
        assert form.is_valid() is False
        assert 'Já existe uma categoria com esta descrição.' in form.errors['description']

    def test_form_permite_mesma_descricao_para_usuario_diferente(self):
        user_one = User.objects.create_user(email='one@example.com', password='StrongPass123')
        user_two = User.objects.create_user(email='two@example.com', password='StrongPass123')
        Category.objects.create(user=user_one, description='Alimentação')

        form = CategoryForm(user=user_two, data={'description': 'ALIMENTAÇÃO'})
        assert form.is_valid() is True

    def test_form_bloqueia_mesma_descricao_na_edicao(self):
        user = User.objects.create_user(email='user@example.com', password='StrongPass123')
        category = Category.objects.create(user=user, description='Transporte')
        form = CategoryForm(user=user, instance=category, data={'description': 'transporte'})
        assert form.is_valid() is False
        assert 'A descrição da categoria não foi alterada.' in form.errors['description']