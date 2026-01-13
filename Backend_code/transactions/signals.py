from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from django.core.mail import send_mail

@receiver(post_save, sender=Transaction)
def send_transaction_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Book Issued",
            f"Hi {instance.user.username}, you issued {instance.book.title}. Due: {instance.due_date}.",
            "library@example.com",
            [instance.user.email],
        )
    elif instance.status == 'RETURNED':
        send_mail(
            "Book Returned",
            f"Hi {instance.user.username}, you returned {instance.book.title}. Fine: Rs {instance.fine_amount}",
            "library@example.com",
            [instance.user.email],
        )



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from .models import Transaction

@receiver(post_save, sender=Transaction)
def send_transaction_email(sender, instance, created, **kwargs):
    """
    Sends email notifications when a book is issued or returned.
    """
    user_email = instance.user.email
    book_title = instance.book.title

    # Book Issued
    if created and instance.status == 'ISSUED':
        subject = "Book Issued Successfully"
        message = (
            f"Hello {instance.user.username},\n\n"
            f"You have successfully issued the book: '{book_title}'.\n"
            f"Issue Date: {instance.issue_date.strftime('%d-%m-%Y')}\n"
            f"Due Date: {instance.due_date.strftime('%d-%m-%Y')}\n\n"
            "Please make sure to return it on time to avoid fines.\n\n"
            "Library Management System"
        )
        send_mail(subject, message, "library@example.com", [user_email])

    # Book Returned
    elif instance.status == 'RETURNED':
        overdue_days = (instance.return_date - instance.due_date).days
        fine_msg = f"Your fine is Rs {instance.fine_amount}" if instance.fine_amount > 0 else "No fine."
        subject = "Book Returned Successfully"
        message = (
            f"Hello {instance.user.username},\n\n"
            f"You have returned the book: '{book_title}'.\n"
            f"Return Date: {instance.return_date.strftime('%d-%m-%Y')}\n"
            f"{fine_msg}\n\n"
            "Thank you for using our Library Management System."
        )
        send_mail(subject, message, "library@example.com", [user_email])
