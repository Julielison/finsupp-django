from django import forms
from django.core.exceptions import ValidationError

from categories.models import Category


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = ('description',)
        widgets = {
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Ex.: Alimentação',
                    'autofocus': True,
                }
            ),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        normalized_description = ' '.join(description.split()).strip().title()

        if self.instance and self.instance.pk:
            current_description = ' '.join((self.instance.description or '').split()).strip().title()
            if normalized_description == current_description:
                raise ValidationError('A descrição da categoria não foi alterada.')

        existing_categories = Category.objects.filter(description__iexact=normalized_description)

        if self.user is not None:
            existing_categories = existing_categories.filter(user=self.user)

        if self.instance and self.instance.pk:
            existing_categories = existing_categories.exclude(pk=self.instance.pk)

        if existing_categories.exists():
            raise ValidationError('Já existe uma categoria com esta descrição.')

        return normalized_description