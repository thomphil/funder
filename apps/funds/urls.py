from django.urls import include, path
from rest_framework import routers

from .api_views import FundViewSet
from .views import (FundCSVListView, FundCSVUploadView, FundDeleteView,
                    FundListView)

router = routers.DefaultRouter()
router.register(r'fund', FundViewSet)


urlpatterns = [
    path('upload/', FundCSVUploadView.as_view(), name='fund-csv-upload'),
    path('queue/', FundCSVListView.as_view(), name='fund-csv-list'),
    path('delete/<int:pk>/', FundDeleteView.as_view(), name='fund-delete'),
    path('api/', include(router.urls)),
    path('', FundListView.as_view(), name='fund-list'),
]
