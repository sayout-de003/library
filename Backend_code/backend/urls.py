# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from books.views import BookViewSet
# from transactions.views import IssueBookView, ReturnBookView, PayFineView, MyHistoryView

# router = DefaultRouter()
# router.register('books', BookViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/transactions/issue/', IssueBookView.as_view()),
#     path('api/transactions/return/', ReturnBookView.as_view()),
#     path('api/transactions/pay-fine/', PayFineView.as_view()),
#     path('api/transactions/my-history/', MyHistoryView.as_view()),
#     path('api/auth/', include('users.urls')),  # we will create users/urls.py
# ]
    

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/transactions/', include('transactions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
