import logging
from datetime import datetime
from typing import Optional

from src import settings
from src.apps.common.enums import RequestMethod, RequestStatus
from src.apps.common.services import RemoteRequest
from src.apps.currenciator.models import Rate

log = logging.getLogger(__name__)


class RateService:
    """Service for retrieving rates for given currency"""

    base_url = settings.BITFINEX.get('BASE_URL')
    # request last 10 days
    history_url = 'candles/trade:1D:t{currency}USD/hist?limit=10'

    @classmethod
    def get_rate(cls, ticker: str, currency_id: int) -> Optional[list]:
        url = f'{cls.base_url}{cls.history_url.format(currency=ticker)}'
        response = RemoteRequest.send(url, data=None, method=RequestMethod.GET)
        if response.status is not RequestStatus.SUCCESS:
            log.error(f'Remote request returned status {response.status}')
            return

        rates = list()
        for idx, response_rate in enumerate(response.json):
            # Convert timestamp from response to datetime
            date = datetime.fromtimestamp(response_rate[0] / 1000)
            # Create Rate instance
            rate = Rate(
                currency_id=currency_id,
                date=date,
                rate=response_rate[2],
                volume=response_rate[-1]
            )
            rates.append(rate)

        # TODO: do not overwrite existing values
        # Write Rate objects in bulk so we don't choke our DB
        rates = Rate.objects.bulk_create(rates)

        return rates
