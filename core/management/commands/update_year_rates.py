import concurrent.futures

from django.core.management.base import BaseCommand
from datetime import date, timedelta, datetime
from currency.views import add_data
from services import Currency


class Command(BaseCommand):
    help = "Update privat bank exchange rates info from year's start"

    def add_arguments(self, parser):
        parser.add_argument('curs', nargs='*', type=str, help='currencies')

    def handle(self, *args, **kwargs):
        curs = kwargs['curs']
        current_date = date.today()-timedelta(hours=12)
        start_of_year = date(current_date.year, 1, 1)
        privatbank = Currency.get_service('PRIVAT', cur_filter=curs)
        self.stdout.write(self.style.WARNING(f'Task started at {datetime.now()}'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for delta in range((current_date - start_of_year).days + 1):
                current_day = (start_of_year + timedelta(days=delta)).strftime("%d.%m.%Y")
                futures.append(executor.submit(privatbank.get_pretty_currency, date=current_day))
                # print(f'Process started for {current_day}')
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                add_data(data)
                self.stdout.write(self.style.WARNING(f"Process finished for {data['exchange_rates'][0]['date']}"))

        # for delta in range((current_date - start_of_year).days + 1):
        #     current_day = (start_of_year + timedelta(days=delta)).strftime("%d.%m.%Y")
        #     data = privatbank.get_pretty_currency(date=current_day)
        #     add_data(data)
        #     print(f"Process finished for {data['exchange_rates'][0]['date']}")

        self.stdout.write(self.style.SUCCESS(f'Task finished at {datetime.now()}'))
