from typing import Optional

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from .models import STRATEGY_CHOICES, Fund, FundCSV


class FundListView(ListView):
    model = Fund
    template_name = 'funds/fund_list.html'
    context_object_name = 'funds'
    _strategy_query_str = None
    strategy_choices = dict(STRATEGY_CHOICES)

    @property
    def strategy_query_str(self) -> Optional[str]:
        """
        Returns the strategy query string if it exists
        """
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


class FundDeleteView(SuccessMessageMixin, UpdateView):
    """
        This performs a soft delete by setting the is_deleted attribute.
    """
    model = Fund
    template_name = 'funds/fund_delete.html'
    fields = ['is_deleted']
    success_message = 'Fund successfully deleted.'

    def get_success_url(self):
        return reverse('fund-list')


class FundCSVUploadView(SuccessMessageMixin, CreateView):
    model = FundCSV
    template_name = 'funds/fund_csv_upload.html'
    fields = ['file']
    success_message = 'Fund CSV file uploaded successfully - this will be processed in the background shortly. See the CSV Queue for status.'

    def get_success_url(self):
        return reverse('fund-csv-list')


class FundCSVListView(ListView):
    model = FundCSV
    template_name = 'funds/fund_csv_list.html'
    context_object_name = 'funds'
    ordering = "-created"
