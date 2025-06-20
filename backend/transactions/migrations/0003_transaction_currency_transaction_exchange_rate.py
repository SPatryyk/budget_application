# Generated by Django 5.2 on 2025-05-23 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.CharField(default='PLN', max_length=3),
        ),
        migrations.AddField(
            model_name='transaction',
            name='exchange_rate',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=12, null=True),
        ),
    ]
