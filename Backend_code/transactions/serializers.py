from rest_framework import serializers
from .models import Transaction, Payment
from books.serializers import BookSerializer

class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
