from rest_framework import serializers
from .models import Goal, GoalTransaction


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name', 'target_amount', 'currency',
                  'current_amount', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at', 'current_amount']


class GoalTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalTransaction
        fields = [
            'id', 'goal', 'type', 'amount', 'currency',
            'description', 'exchange_rate', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
