# django-currency
### Installation
1. Clone the repository
   ```
   git clone https://github.com/Britva4ka/django-currency.git
   ```
2. Create venv
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```
3. Install project dependencies
   ```
   pip install -r requirements.txt
   ```
4. Copy `env.example` to `.env` with initial configurations
   ```
   cp env.example .env
   ```
### Setup database
Upgrade SQLite db to latest version
```
python3 manage.py migrate
```
## READY TO USE
Run server
```
python3 manage.py runserver
```
### Commands
1. Retrieve the exchange rates for the required currencies from PrivatBank starting from the beginning of the year:
   ```
   python3 manage.py update_year_rates
   ```
   By default, required currencies are: "GBP, USD, CHF, EUR".
   ***
   You can also choose yours, for example:
   ```
   python3 manage.py update_year_rates PLN AZN
   ```