from datetime import timedelta

from django.db import models
from django.db.models import Avg
from django.db.models import deletion
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from src.apps.currenciator.models import Currency


class Rate(models.Model):
    """Currency Rate model"""

    currency = models.ForeignKey(
        Currency,
        blank=True,
        null=True,
        on_delete=deletion.PROTECT,
        related_name='rates',
        verbose_name=_('Валюта'),
    )
    date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Дата'),
    )
    rate = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Курс к USD'),
    )
    volume = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Объём торгов за день'),
    )

    class Meta:
        verbose_name = _('Курс валют')
        verbose_name_plural = _('Курсы валют')

    def __str__(self):
        return f'{self.id} {self.date}'

    @property
    def avg_volume(self):
        """Returns average volume for the pas ten days"""
        ten_days_ago = timezone.now() - timedelta(days=10)
        avg_volume = Rate.objects.filter(
            date__gte=ten_days_ago
        ).aggregate(Avg('volume'))

        return avg_volume.get('volume__avg')
