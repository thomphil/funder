from django.core.management.base import BaseCommand
from ...models import Fund, FundCSV


class Command(BaseCommand):
    def handle(self, *args, **options):
            self.stdout.write(self.style.SUCCESS('Process Uploads - Running'))

            # get first pending CSV
            fund_csv = FundCSV.objects.filter(status='pending').first()

            if not fund_csv:
                self.stdout.write(self.style.SUCCESS('No pending CSV files'))
                self.stdout.write(self.style.SUCCESS('Process Uploads - Complete'))
                return

            # set status to processing
            fund_csv.status = 'processing'
            fund_csv.save()

            # get fund csv row objects
            funds = fund_csv.get_row_objects()

            # for each object create Fund instance
            fund_objects = [Fund(**fund.dict()) for fund in funds]

            try:
                Fund.objects.bulk_create(fund_objects)
                fund_csv.status = 'processed'
                fund_csv.save()
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(e))
                self.stdout.write(self.style.SUCCESS('Process Uploads - Complete'))
                fund_csv.status = 'error'
                fund_csv.save()
                return

            self.stdout.write(self.style.SUCCESS('Process Uploads - Complete'))