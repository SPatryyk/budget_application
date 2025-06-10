from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        return Category.objects.create(user=user, **validated_data)


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TransactionSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source='category'
    )

    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'type', 'amount', 'currency', 'exchange_rate',
                  'category', 'category_id', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']
