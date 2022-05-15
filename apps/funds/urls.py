from django.urls import include, path
from django.urls import path
from .views import (FundCSVListView, FundCSVUploadView, FundDeleteView,
                    FundListView)

from .views import FundCSVListView, FundCSVUploadView, FundListView

urlpatterns = [
    path('upload/', FundCSVUploadView.as_view(), name='fund-csv-upload'),
    path('queue/', FundCSVListView.as_view(), name='fund-csv-list'),
    path('delete/<int:pk>/', FundDeleteView.as_view(), name='fund-delete'),
    path('', FundListView.as_view(), name='fund-list'),
]
