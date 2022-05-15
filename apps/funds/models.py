from django.db import models

STRATEGY_CHOICES = (
    ('equity', 'Long/Short Equity'),
    ('global', 'Global Macro'),
    ('arbitrage', 'Arbitrage'),
)

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