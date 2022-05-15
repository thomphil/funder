from rest_framework import viewsets

from .models import Fund
from .serializers import FundSerializer


class FundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        strategy_query = self.request.query_params.get('strategy')

        if strategy_query:
            qs = qs.filter(strategy=strategy_query)

        return qs
