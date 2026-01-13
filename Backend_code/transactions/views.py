# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import viewsets
# from .models import Transaction, Payment
# from .serializers import TransactionSerializer, PaymentSerializer
# from books.models import Book
# from users.models import User
# from django.utils import timezone

# class IssueBookView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         book_id = request.data.get('book_id')
#         book = Book.objects.get(id=book_id)
#         if book.available_quantity <= 0:
#             return Response({'error': 'Book not available'}, status=400)
#         transaction = Transaction.objects.create(user=request.user, book=book)
#         book.available_quantity -= 1
#         book.save()
#         serializer = TransactionSerializer(transaction)
#         return Response(serializer.data)

# class ReturnBookView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         transaction_id = request.data.get('transaction_id')
#         transaction = Transaction.objects.get(id=transaction_id, user=request.user)
#         if transaction.status == 'RETURNED':
#             return Response({"detail": "Already returned."}, status=400)
#         today = timezone.now()
#         overdue_days = (today - transaction.due_date).days
#         transaction.fine_amount = max(0, overdue_days * 5)
#         transaction.status = 'RETURNED'
#         transaction.return_date = today
#         transaction.book.available_quantity += 1
#         transaction.book.save()
#         transaction.save()
#         serializer = TransactionSerializer(transaction)
#         return Response(serializer.data)

# class PayFineView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         transaction_id = request.data.get('transaction_id')
#         amount = request.data.get('amount')
#         transaction = Transaction.objects.get(id=transaction_id, user=request.user)
#         payment = Payment.objects.create(
#             transaction=transaction,
#             amount=amount,
#             transaction_id="DUMMY123",
#             status='SUCCESS'
#         )
#         serializer = PaymentSerializer(payment)
#         return Response(serializer.data)

# class MyHistoryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         transactions = Transaction.objects.filter(user=request.user)
#         serializer = TransactionSerializer(transactions, many=True)
#         return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Transaction, Payment
from .serializers import TransactionSerializer, PaymentSerializer
from books.models import Book
from django.utils import timezone

# Issue Book
class IssueBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        if book.available_quantity <= 0:
            return Response({'error': 'Book not available'}, status=400)
        transaction = Transaction.objects.create(user=request.user, book=book)
        book.available_quantity -= 1
        book.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

# Return Book
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        if transaction.status == 'RETURNED':
            return Response({"detail": "Already returned."}, status=400)
        today = timezone.now()
        overdue_days = (today - transaction.due_date).days
        transaction.fine_amount = max(0, overdue_days * 5)
        transaction.status = 'RETURNED'
        transaction.return_date = today
        transaction.book.available_quantity += 1
        transaction.book.save()
        transaction.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

# Pay Fine
class PayFineView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        amount = request.data.get('amount')
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        payment = Payment.objects.create(
            transaction=transaction,
            amount=amount,
            transaction_id="DUMMY123",
            status='SUCCESS'
        )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

# Member History
class MyHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

# Admin: All Transactions
class AllTransactionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
