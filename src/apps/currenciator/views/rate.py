from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from src.apps.currenciator.models import Rate, Currency
from src.apps.currenciator.serializers import RateSerializer
from src.apps.currenciator.services import RateService


class RateView(RetrieveAPIView):
    """View for specified currency rate"""
    serializer_class = RateSerializer

    def retrieve(self, request, *args, **kwargs):
        currency_id = request.query_params.get('id')
        # throw 400 if ID is not provided
        if not currency_id:
            context = {'error': 'id is missing in query params'}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        currency = get_object_or_404(Currency, id=currency_id)

        rate = Rate.objects.filter(
            currency_id=currency_id,
            date=timezone.now()
        )
        # Populate rates if there is no values
        if not rate.exists():
            RateService.get_rate(currency.name, currency_id)

        context = self.serializer_class(rate.get()).data

        return Response(context)
