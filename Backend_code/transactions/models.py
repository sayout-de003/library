from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User
from books.models import Book

class Transaction(models.Model):
    STATUS_CHOICES = [('ISSUED', 'Issued'), ('RETURNED', 'Returned')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=15))
    return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ISSUED')

# class Payment(models.Model):
#     STATUS_CHOICES = [('SUCCESS', 'Success'), ('FAILED', 'Failed')]
#     transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_ref = models.CharField(max_length=255)  # renamed
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Payment(models.Model):
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    payment_reference = models.CharField(
        max_length=50,
        unique=True
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("SUCCESS", "SUCCESS"), ("FAILED", "FAILED")]
    )

    def __str__(self):
        return f"{self.payment_reference} - {self.amount}"
