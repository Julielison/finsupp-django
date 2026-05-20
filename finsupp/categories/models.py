from django.conf import settings
from django.db import models


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True,
    )
    description = models.CharField('descrição', max_length=15)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['description']
        constraints = [
            models.UniqueConstraint(fields=['user', 'description'], name='unique_category_per_user'),
        ]

    def save(self, *args, **kwargs):
        if self.description:
            normalized_description = ' '.join(self.description.split()).strip().title()
            self.description = normalized_description
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description