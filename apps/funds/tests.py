from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase

from .models import Fund, FundCSV


def get_test_csv(file_label):
    file_name = f'apps/funds/testCSVs/{file_label}.csv'
    with open(file_name, 'r') as f:
        file = SimpleUploadedFile(
            name=f'{file_label}.csv',
            content=f.read().encode('utf-8-sig'),
        )
        return file


class FundCSVTestCase(TestCase):
    def test_fund_csv_with_valid_file_success(self):
        file = get_test_csv('valid')
        fund_csv = FundCSV(file=file)
        fund_csv.clean_file()

    def test_fund_csv_with_negative_aum_fails(self):
        file = get_test_csv('negative_aum')
        fund_csv = FundCSV(file=file)
        self.assertRaises(ValidationError, fund_csv.full_clean)

    def test_fund_csv_with_incorrect_strategy_fails(self):
        file = get_test_csv('invalid_strategy')
        fund_csv = FundCSV(file=file)
        self.assertRaises(ValidationError, fund_csv.full_clean)

    def test_fund_csv_with_blank_name_fails(self):
        file = get_test_csv('blank_name')
        fund_csv = FundCSV(file=file)
        self.assertRaises(ValidationError, fund_csv.full_clean)

    def test_fund_csv_generated_correctly_named_funds(self):
        file = get_test_csv('valid')
        fund_csv = FundCSV(file=file)
        fund_csv.save()

        call_command("process_uploads")

        # All the Fund names in the CSV
        fund_names = [fund.name for fund in fund_csv.get_row_objects()]

        total_correctly_named_funds = sum(
            [1 for fund in Fund.objects.all() if fund.name in fund_names]
        )

        self.assertEqual(total_correctly_named_funds, len(fund_names))






