from rest_framework import serializers
from .models import Wallet, Transfer


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'balance', 'currency', 'type', 'created_at']
        read_only_fields = ['id', 'created_at', 'balance']


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            'id', 'from_wallet', 'from_goal',
            'to_wallet', 'to_goal',
            'amount', 'description', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
