from rest_framework.generics import ListAPIView

from src.apps.currenciator.models import Currency
from src.apps.currenciator.serializers import CurrencySerializer


class CurrencyListView(ListAPIView):
    """View for listing all currencies"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
