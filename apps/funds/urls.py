from django.urls import path

from .views import FundCSVListView, FundCSVUploadView, FundListView

urlpatterns = [
    path('upload/', FundCSVUploadView.as_view(), name='fund-csv-upload'),
    path('queue/', FundCSVListView.as_view(), name='fund-csv-list'),
    path('', FundListView.as_view(), name='fund-list'),
]
