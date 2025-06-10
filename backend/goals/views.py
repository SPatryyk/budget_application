from rest_framework import generics, permissions, serializers
from .models import Goal, GoalTransaction
from .serializers import GoalSerializer, GoalTransactionSerializer
from core.utils import get_exchange_rate
from decimal import Decimal


class GoalListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalTransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = GoalTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        goal_id = self.request.query_params.get('goal')
        if not goal_id:
            return GoalTransaction.objects.none()
        return GoalTransaction.objects.filter(
            user=self.request.user, goal__id=goal_id
        ).order_by('-created_at')

    def perform_create(self, serializer):
        data = serializer.validated_data
        goal = data['goal']
        input_amount = data['amount']
        input_currency = data['currency']
        transaction_type = data['type']

        if input_currency == goal.currency:
            rate = 1.0
        else:
            rate = get_exchange_rate(input_currency, goal.currency)
            if rate is None:
                raise serializers.ValidationError(
                    f"Nie udało się pobrać kursu {input_currency} → {goal.currency}.")

        converted_amount = Decimal(input_amount) * Decimal(rate)

        transaction = serializer.save(
            user=self.request.user,
            amount=converted_amount,
            exchange_rate=rate
        )

        if transaction_type == 'deposit':
            goal.current_amount += converted_amount
        elif transaction_type == 'withdrawal':
            goal.current_amount -= converted_amount

        goal.save()
