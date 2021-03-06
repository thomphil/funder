# Generated by Django 3.2 on 2022-05-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('strategy', models.CharField(choices=[('equity', 'Long/Short Equity'), ('global', 'Global Macro'), ('arbitrage', 'Arbitrage')], max_length=100)),
                ('aum', models.IntegerField(blank=True, null=True)),
                ('inception_date', models.DateField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
