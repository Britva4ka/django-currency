import time
from datetime import datetime, timedelta
from json import JSONDecodeError
from colorama import init, Fore
import pycountry
import requests as requests
init()


class Currency:
    """
    SERVICE SELECTOR.
    Usage:
    bank = Currency.get_service('bank')
    """
    currency_list = []
    url = ''

    @classmethod
    def get_service(cls, call: str, cur_filter=None):
        """
        select provider service
        :param call: name of provider
        :param cur_filter: not necessary. Changes currencies filter
        :return: init class of needed service.
        """
        if cur_filter is None or not cur_filter:
            cls.currency_list = ["GBP", "USD", "CHF", "EUR"]
        elif isinstance(cur_filter, list) and cur_filter and all(isinstance(item, str)
                                                                 and len(item) == 3 for item in cur_filter):
            cls.currency_list = [item.upper() for item in cur_filter]
            print(Fore.MAGENTA + f'Filter set {cls.currency_list}' + Fore.RESET)
        else:
            raise TypeError(Fore.RED + "cur_filter must be a list of strings with length 3" + Fore.RESET)
        if call == "PRIVAT":
            cls.params = {
                "date": (datetime.now()-timedelta(hours=12)).strftime("%d.%m.%Y"),
            }
            return PrivatBank()
        elif call == "MONO":
            cls.params = {
                "date": '',
            }
            return MonoBank()
        else:
            raise NotImplementedError(Fore.RED + f"no such service {call}" + Fore.RESET)

    def get_api_info(self, **kwargs):
        """
        Only after selecting service!

        Sending request to chosen service and handle answer.
        :return: response in json format.
        """
        if not self.url:
            raise Exception(Fore.RED + 'Select service first.' + Fore.RESET)
        response = requests.get(self.url, params={key: value for key, value in kwargs.items()} or self.params)
        try:
            response.raise_for_status()
            data = response.json()
            print(Fore.GREEN + f'GOT API DATA FOR '
                               f'{kwargs.get("date") or self.params["date"] or datetime.now().strftime("%d.%m.%Y")}'
                  + Fore.RESET)
            return data
        except JSONDecodeError as e:
            print(Fore.RED + f"JSON decoding error: {e}" + Fore.RESET)
            raise
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Request error: {e},\nRetry in 3 seconds..." + Fore.RESET)
            time.sleep(3)
            self.get_api_info(**kwargs)

    def get_currency(self, **kwargs):
        """
        Only after selecting service!

        Make request to server, handle answer, filter data.
        :return: filtered data from response.
        """
        raise NotImplementedError

    def get_pretty_currency(self, **kwargs):
        """
        Only after selecting service!

        :return: pretty data for db save.
        """
        raise NotImplementedError

    def set_currency_filter_list(self, cur_filter: list):
        """
        Function for edit filter if u want.
        :param cur_filter: list of required currencies
        :return: set new currency_list filter
        """
        if all(isinstance(item, str) and len(item) == 3 for item in cur_filter):
            self.currency_list = [item.upper() for item in cur_filter]
        else:
            raise NotImplementedError


class PrivatBank(Currency):

    url = "https://api.privatbank.ua/p24api/exchange_rates"

    def get_currency(self, **kwargs):
        data = self.get_api_info(**kwargs)
        currencies = data["exchangeRate"]
        filtered_currencies = [{**cur, "date": data['date']} for cur in currencies if cur["currency"]
                               in self.currency_list and cur["baseCurrency"] == 'UAH']
        if not filtered_currencies:
            print(Fore.RED + "Needed currencies not found." + Fore.RESET)
        return filtered_currencies

    def get_pretty_currency(self, **kwargs):
        data = self.get_currency(**kwargs)
        currency_data = [{
            "base_currency": item["baseCurrency"],
            "currency": item["currency"],
            "buy_rate": item['purchaseRate'],
            "sell_rate": item['saleRate'],
            "date": datetime.strptime(item['date'], '%d.%m.%Y').strftime("%Y-%m-%d")
        } for item in data]

        pretty_data = {
            "provider": "PRIVAT",
            "api_url": self.url,
            "exchange_rates": currency_data
        }
        return pretty_data


class MonoBank(Currency):

    url = "https://api.monobank.ua/bank/currency"

    def get_currency(self, **kwargs):
        currency_list_codes = [int(pycountry.currencies.get(alpha_3=cur).numeric) for cur in self.currency_list]
        data = self.get_api_info(**kwargs)
        filtered_currencies = [cur for cur in data if cur["currencyCodeA"] in currency_list_codes and
                               cur["currencyCodeB"] == 980]
        return filtered_currencies

    def get_pretty_currency(self, **kwargs):
        data = self.get_currency(**kwargs)

        currency_data = [{
            "base_currency": pycountry.currencies.get(numeric=str(item['currencyCodeB'])).alpha_3,
            "currency": pycountry.currencies.get(numeric=str(item['currencyCodeA'])).alpha_3,
            "buy_rate": item['rateBuy'],
            "sell_rate": item['rateSell'],
            "date": datetime.fromtimestamp(item['date']).strftime("%Y-%m-%d")
        } for item in data]

        pretty_data = {
            "provider": "MONO",
            "api_url": self.url,
            "exchange_rates": currency_data
        }
        return pretty_data


if __name__ == "__main__":
    bank = Currency.get_service('MONO')
    data = bank.get_pretty_currency()
    print(data)
    # u can run this file for test
