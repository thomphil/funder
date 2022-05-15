from django.db.models import Sum
from django.views.generic import ListView

from .models import STRATEGY_CHOICES, Fund


class FundListView(ListView):
    model = Fund
    template_name = 'funds/fund_list.html'
    context_object_name = 'funds'
    _strategy_query_str = None
    strategy_choices = dict(STRATEGY_CHOICES)

    @property
    def strategy_query_str(self):
        if self._strategy_query_str:
            return self._strategy_query_str

        strategy = self.request.GET.get('strategy')
        
        if strategy in self.strategy_choices:
            self._strategy_query_str = strategy
        return self._strategy_query_str

    def get_queryset(self):
        qs = super().get_queryset()

        if self.strategy_query_str:
            qs = qs.filter(strategy=self.strategy_choices[self.strategy_query_str])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funds_count'] = context['funds'].count()
        context['aum_sum'] = context['funds'].aggregate(aum_sum=Sum('aum')).get('aum_sum')

        context['strategy_choices'] = STRATEGY_CHOICES

        if self.strategy_query_str:
            context['current_strategy'] = self.strategy_query_str

        return context
