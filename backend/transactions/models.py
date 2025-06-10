import uuid
from django.db import models
from django.conf import settings
from wallets.models import Wallet


class Category(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Przychód'),
        ('expense', 'Wydatek'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True, blank=True
    )
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Przychód'),
        ('expense', 'Wydatek'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, default='PLN')
    exchange_rate = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.wallet.name})"
