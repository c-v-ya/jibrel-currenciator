from .currency_list import CurrencyListView
from .rate import RateView

currency_list_view = CurrencyListView.as_view()  # list currencies
rate_view = RateView.as_view()  # currency rate info
