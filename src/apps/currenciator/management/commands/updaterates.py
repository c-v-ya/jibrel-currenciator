import logging

from django.core.management import BaseCommand
from django.utils import timezone

from src.apps.currenciator.models import Currency
from src.apps.currenciator.services import RateService

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update rates for every currency without rate in DB'

    def handle(self, *args, **options):
        now = timezone.now()
        currencies = Currency.objects.exclude(
            rates__date=now
        ).prefetch_related('rates')
        log.info(f'Updating rates for {currencies.count()} currencies')

        for currency in currencies:
            RateService.get_rate(currency.name, currency.id)
