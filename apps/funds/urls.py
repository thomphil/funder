from django.urls import path
from .views import FundListView

urlpatterns = [
    path('', FundListView.as_view(), name='fund-list'),
]
