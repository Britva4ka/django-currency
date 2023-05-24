from django.shortcuts import render
from .models import Bank, ExchangeRate
from services import Currency
from colorama import init, Fore
# Create your views here.
init()


def add_data(data: dict):
    """
    ONLY FOR DATA FROM GET_PRETTY_CURRENCY
    :param data: pretty_data
    :return: db update
    """
    bank, created = Bank.objects.get_or_create(provider=data['provider'], api_url=data['api_url'])
    exchange_rates = [ExchangeRate(bank=bank, **item) for item in data["exchange_rates"]
                      if not ExchangeRate.objects.filter(bank=bank, **item).exists()]
    ExchangeRate.objects.bulk_create(exchange_rates)


def currency(request):
    monobank = Currency.get_service('MONO')
    try:
        data = monobank.get_pretty_currency()
        print(data)
        add_data(data)
        print(Fore.GREEN + 'SAVED TO DATABASE.' + Fore.RESET)
    except Exception as e:
        print('Error:' + str(e))

    privatbank = Currency.get_service('PRIVAT')
    try:
        data = privatbank.get_pretty_currency()
        print(data)
        add_data(data)
        print(Fore.GREEN + 'SAVED TO DATABASE.' + Fore.RESET)
    except Exception as e:
        print('Error:' + str(e))

    context = {
        'hello': 'hello'
    }
    return render(request, template_name='core/currency.html', context=context)
