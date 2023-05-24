# Generated by Django 4.2.1 on 2023-05-19 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=100, unique=True)),
                ('api_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=10)),
                ('currency', models.CharField(max_length=10)),
                ('buy_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default='19.05.2023')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.bank')),
            ],
        ),
    ]
