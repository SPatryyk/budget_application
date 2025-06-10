import uuid
from django.db import models
from django.conf import settings


class Wallet(models.Model):
    WALLET_TYPES = (
        ('cash', 'Gotówka'),
        ('bank', 'Konto bankowe'),
        ('saving', 'Konto oszczędnościowe'),
        ('investment', 'Inwestycje'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3)
    type = models.CharField(max_length=20, choices=WALLET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.currency})"


class Transfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='transfers')

    from_wallet = models.ForeignKey(
        'Wallet', on_delete=models.SET_NULL, null=True, blank=True, related_name='outgoing_transfers')
    to_wallet = models.ForeignKey('Wallet', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='incoming_transfers')

    from_goal = models.ForeignKey('goals.Goal', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='outgoing_transfers')
    to_goal = models.ForeignKey('goals.Goal', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='incoming_transfers')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} transfer {self.amount}"
