from rest_framework import generics, permissions, serializers
from django.db.models import Q
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer
from core.utils import get_exchange_rate
from decimal import Decimal


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            Q(user=self.request.user) | Q(user__isnull=True)
        )


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data
        wallet = data['wallet']
        input_amount = data['amount']
        input_currency = data['currency']
        transaction_type = data['type']

        # Obliczamy kurs i przeliczoną kwotę
        if input_currency == wallet.currency:
            rate = 1.0
        else:
            rate = get_exchange_rate(
                base_currency=input_currency, target_currency=wallet.currency)
            if rate is None:
                raise serializers.ValidationError(
                    f"Nie udało się pobrać kursu {input_currency} → {wallet.currency}.")

        converted_amount = input_amount * Decimal(rate)

        transaction = serializer.save(
            user=self.request.user,
            amount=converted_amount,
            exchange_rate=rate
        )

        if transaction_type == 'income':
            wallet.balance += converted_amount
        elif transaction_type == 'expense':
            wallet.balance -= converted_amount

        wallet.save()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
