import csv
import io

from django.db import models
from django.core.exceptions import ValidationError

from .validators import FundCSVRow

STRATEGY_CHOICES = (
    ('equity', 'Long/Short Equity'),
    ('global', 'Global Macro'),
    ('arbitrage', 'Arbitrage'),
)

CSV_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('processed', 'Processed'),
    ('error', 'Error'),
)

CSV_FIELD_NAMES = {
    'Name': 'name',
    'Strategy': 'strategy',
    'AUM (USD)': 'aum',
    'Inception Date': 'inception_date',
}


class FundManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Fund(models.Model):
    objects = FundManager()
    
    name = models.CharField(
        max_length=100
    )

    strategy = models.CharField(
        max_length=100,
        choices=STRATEGY_CHOICES,
    )

    aum = models.IntegerField(
        null=True,
        blank=True,
    )

    inception_date = models.DateField(
        null=True,
        blank=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    
class FundCSV(models.Model):
    file = models.FileField(
        upload_to='uploads/csv/',
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=100,
        default='pending',
    )
