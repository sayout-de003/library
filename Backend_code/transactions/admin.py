from django.contrib import admin
from .models import Transaction, Payment

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'status', 'issue_date', 'due_date', 'return_date', 'fine_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')
    ordering = ('-issue_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'amount', 'status', 'payment_date', 'transaction_id')
    list_filter = ('status',)
    search_fields = ('transaction__user__username', 'transaction__book__title', 'transaction_id')
    ordering = ('-payment_date',)
