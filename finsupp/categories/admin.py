from django.contrib import admin

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user')
    search_fields = ('description', 'user__email')
    ordering = ('description',)