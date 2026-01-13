from django.urls import path
from .views import IssueBookView, ReturnBookView, PayFineView, MyHistoryView, AllTransactionsView

urlpatterns = [
    path('issue/', IssueBookView.as_view(), name='issue-book'),
    path('return/', ReturnBookView.as_view(), name='return-book'),
    path('pay-fine/', PayFineView.as_view(), name='pay-fine'),
    path('my-history/', MyHistoryView.as_view(), name='my-history'),
    path('all/', AllTransactionsView.as_view(), name='all-transactions'),  # Admin only
]
