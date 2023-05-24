from django.db import models
# Create your models here.


class Bank(models.Model):
    provider = models.CharField(max_length=100, unique=True)
    api_url = models.URLField()

    def __str__(self):
        return self.provider


class ExchangeRate(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=2)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=False)

    def __str__(self):
        return f"{self.bank} - {self.currency}: {self.buy_rate}/{self.sell_rate} for {self.date}"
