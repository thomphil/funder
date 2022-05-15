from django.urls import include, path
from .conjob import conjob


urlpatterns = [
    path('', include('apps.funds.urls')),
]

conjob()