from django.urls import path

from src.apps.currenciator.views import currency_list_view, rate_view

"""API views for Currenciator project"""

app_name = 'currenciator'
urlpatterns = [
    path('currencies', currency_list_view, name='currency_list'),
    path('rate/', rate_view, name='rate'),
]
