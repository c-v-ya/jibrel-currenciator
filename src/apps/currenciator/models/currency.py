from django.db import models

from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    """Currency model"""

    name = models.CharField(
        blank=True,
        max_length=20,
        null=True,
        verbose_name=_('Наименование'),
    )

    class Meta:
        verbose_name = _('Валюта')
        verbose_name_plural = _('Валюты')

    def __str__(self):
        return f'{self.id} {self.name}'
