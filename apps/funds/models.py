import csv
import io
from tempfile import TemporaryFile
from typing import List

from django.core.exceptions import ValidationError
from django.db import models

from .validators import FundCSVRow

# Define DictReader type for use with Type annotations
with TemporaryFile() as t:
    CSVDictReader = type(csv.DictReader(t))


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

    def get_csv_reader(self) -> CSVDictReader:
        decoded_file = self.file.read().decode("utf-8-sig")
        io_string = io.StringIO(decoded_file)
        csv_reader = csv.DictReader(io_string)

        return csv_reader

    def get_row_objects(self) -> List[FundCSVRow]:
        csv_reader = self.get_csv_reader()

        rows = [FundCSVRow.parse_args(row.values()) for row in csv_reader]
        return rows

    def clean_file(self) -> None:
        try:
            self.get_row_objects()
        except ValueError as e:
            raise ValidationError(e)

    def clean(self):
        self.clean_file()
