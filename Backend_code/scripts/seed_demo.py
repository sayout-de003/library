from users.models import User
from books.models import Book
from transactions.models import Transaction, Payment
from django.utils import timezone
from datetime import timedelta
import random

# -----------------------
# Admin
# -----------------------
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123",
        role="ADMIN"
    )
    print("✅ Admin created")

# -----------------------
# Members
# -----------------------
member_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah"]

for name in member_names:
    if not User.objects.filter(username=name.lower()).exists():
        User.objects.create_user(
            username=name.lower(),
            email=f"{name.lower()}@example.com",
            password="member123",
            role="MEMBER",
            phone=f"+91{random.randint(7000000000, 9999999999)}",
            address=f"{random.randint(1,999)} Demo Street"
        )

print("✅ Members created")

# -----------------------
# Books (NO PDF)
# -----------------------
categories = ["Fiction", "Science", "Math", "History", "Biography", "Fantasy", "Technology"]

books_data = [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565"),
    ("1984", "George Orwell", "9780451524935"),
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084"),
    ("A Brief History of Time", "Stephen Hawking", "9780553380163"),
    ("The Art of Computer Programming", "Donald Knuth", "9780201896831"),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "9780590353427"),
    ("Clean Code", "Robert C. Martin", "9780132350884"),
    ("The Hobbit", "J.R.R. Tolkien", "9780345339683"),
]

for title, author, isbn in books_data:
    if not Book.objects.filter(isbn=isbn).exists():
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            category=random.choice(categories),
            quantity=10,
            available_quantity=10
        )

print("✅ Books created")

# -----------------------
# Transactions + Payments
# -----------------------
members = User.objects.filter(role="MEMBER")
books = Book.objects.all()

for _ in range(12):
    user = random.choice(members)
    book = random.choice(books)
    issued_days_ago = random.randint(1, 25)

    issue_date = timezone.now() - timedelta(days=issued_days_ago)
    due_date = issue_date + timedelta(days=15)

    returned = random.choice([True, False])

    txn = Transaction.objects.create(
        user=user,
        book=book,
        issue_date=issue_date,
        due_date=due_date,
        return_date=timezone.now() if returned else None,
        status="RETURNED" if returned else "ISSUED"
    )

    if returned and issue_date + timedelta(days=15) < timezone.now():
        overdue_days = (timezone.now() - due_date).days
        fine = overdue_days * 5
        txn.fine_amount = fine
        txn.save()

        Payment.objects.create(
            transaction=txn,
            amount=fine,
            payment_date=timezone.now(),
            transaction_id=f"TXN{random.randint(10000,99999)}",
            status="SUCCESS"
        )

print("🎉 Demo data seeded successfully")

