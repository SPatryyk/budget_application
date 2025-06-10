from rest_framework import generics, permissions, serializers
from .models import Wallet, Transfer
from .serializers import WalletSerializer
from .serializers import TransferSerializer
from transactions.models import Transaction
from goals.models import GoalTransaction
from core.utils import get_exchange_rate
from decimal import Decimal


class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)


class TransferListCreateView(generics.ListCreateAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        wallet_id = self.request.query_params.get('wallet')
        if wallet_id:
            queryset = queryset.filter(wallet__id=wallet_id)
        return queryset

    def perform_create(self, serializer):
        transfer = serializer.save(user=self.request.user)
        amount = transfer.amount

        if transfer.from_wallet:
            from_currency = transfer.from_wallet.currency

            if transfer.to_wallet:
                to_currency = transfer.to_wallet.currency
                rate = 1.0 if from_currency == to_currency else get_exchange_rate(
                    from_currency, to_currency)
                if rate is None:
                    raise serializers.ValidationError(
                        f"Nie udało się pobrać kursu {from_currency} → {to_currency}.")
                converted_amount = Decimal(amount) * Decimal(rate)

                transfer.from_wallet.balance -= amount
                transfer.to_wallet.balance += converted_amount
                transfer.from_wallet.save()
                transfer.to_wallet.save()

                Transaction.objects.create(
                    user=self.request.user,
                    wallet=transfer.from_wallet,
                    type='expense',
                    amount=amount,
                    currency=from_currency,
                    exchange_rate=rate,
                    description=f"Transfer do: {transfer.to_wallet}",
                    date=transfer.date
                )
                Transaction.objects.create(
                    user=self.request.user,
                    wallet=transfer.to_wallet,
                    type='income',
                    amount=converted_amount,
                    currency=to_currency,
                    exchange_rate=rate,
                    description=f"Transfer od: {transfer.from_wallet}",
                    date=transfer.date
                )

            if transfer.to_goal:
                to_currency = transfer.to_goal.currency
                rate = 1.0 if from_currency == to_currency else get_exchange_rate(
                    from_currency, to_currency)
                if rate is None:
                    raise serializers.ValidationError(
                        f"Nie udało się pobrać kursu {from_currency} → {to_currency}.")
                converted_amount = Decimal(amount) * Decimal(rate)

                transfer.from_wallet.balance -= amount
                transfer.from_wallet.save()
                transfer.to_goal.current_amount += converted_amount
                transfer.to_goal.save()

                GoalTransaction.objects.create(
                    goal=transfer.to_goal,
                    user=self.request.user,
                    type='deposit',
                    amount=converted_amount,
                    currency=to_currency,
                    exchange_rate=rate,
                    description=transfer.description,
                    date=transfer.date
                )

        if transfer.from_goal:
            from_currency = transfer.from_goal.currency

            if transfer.to_wallet:
                to_currency = transfer.to_wallet.currency
                rate = 1.0 if from_currency == to_currency else get_exchange_rate(
                    from_currency, to_currency)
                if rate is None:
                    raise serializers.ValidationError(
                        f"Nie udało się pobrać kursu {from_currency} → {to_currency}.")
                converted_amount = Decimal(amount) * Decimal(rate)

                transfer.from_goal.current_amount -= amount
                transfer.from_goal.save()
                transfer.to_wallet.balance += converted_amount
                transfer.to_wallet.save()

                Transaction.objects.create(
                    user=self.request.user,
                    wallet=transfer.to_wallet,
                    type='income',
                    amount=converted_amount,
                    currency=to_currency,
                    exchange_rate=rate,
                    description=f"Transfer od: {transfer.from_goal}",
                    date=transfer.date
                )
                GoalTransaction.objects.create(
                    goal=transfer.from_goal,
                    user=self.request.user,
                    type='withdrawal',
                    amount=amount,
                    currency=from_currency,
                    exchange_rate=rate,
                    description=transfer.description,
                    date=transfer.date
                )

            if transfer.to_goal:
                to_currency = transfer.to_goal.currency
                rate = 1.0 if from_currency == to_currency else get_exchange_rate(
                    from_currency, to_currency)
                if rate is None:
                    raise serializers.ValidationError(
                        f"Nie udało się pobrać kursu {from_currency} → {to_currency}.")
                converted_amount = Decimal(amount) * Decimal(rate)

                transfer.from_goal.current_amount -= amount
                transfer.from_goal.save()
                transfer.to_goal.current_amount += converted_amount
                transfer.to_goal.save()

                GoalTransaction.objects.create(
                    goal=transfer.from_goal,
                    user=self.request.user,
                    type='withdrawal',
                    amount=amount,
                    currency=from_currency,
                    exchange_rate=rate,
                    description=transfer.description,
                    date=transfer.date
                )
                GoalTransaction.objects.create(
                    goal=transfer.to_goal,
                    user=self.request.user,
                    type='deposit',
                    amount=converted_amount,
                    currency=to_currency,
                    exchange_rate=rate,
                    description=transfer.description,
                    date=transfer.date
                )


class TransferDetailView(generics.RetrieveAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transfer.objects.filter(user=self.request.user)
