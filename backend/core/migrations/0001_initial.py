# Generated by Django 5.2 on 2025-05-23 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=3)),
                ('target_currency', models.CharField(max_length=3)),
                ('rate', models.DecimalField(decimal_places=6, max_digits=12)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'unique_together': {('base_currency', 'target_currency')},
            },
        ),
    ]
