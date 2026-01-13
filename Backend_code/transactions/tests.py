from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Transaction, Payment
from books.models import Book

User = get_user_model()


class TransactionAPITest(APITestCase):
    """Comprehensive tests for Transaction API"""

    def setUp(self):
        """Set up test data"""
        # Create admin user
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="Admin@123"
        )
        
        # Create member user
        self.member = User.objects.create_user(
            username="member",
            email="member@test.com",
            password="Member@123"
        )
        
        # Create another member
        self.member2 = User.objects.create_user(
            username="member2",
            email="member2@test.com",
            password="Member2@123"
        )
        
        # Create a librarian user
        self.librarian = User.objects.create_user(
            username="librarian",
            email="librarian@test.com",
            password="Librarian@123",
            role="ADMIN"
        )
        
        # Create book payload
        self.book_payload = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "category": "Programming",
            "isbn": "9780132350884",
            "total_copies": 5,
            "available_copies": 5,
            "description": "A handbook of agile software craftsmanship",
            "cover_image": None
        }
        
        self.book_payload_limited = {
            "title": "Limited Book",
            "author": "Test Author",
            "category": "Testing",
            "isbn": "9780132350885",
            "total_copies": 1,
            "available_copies": 1,
            "description": "A book with limited copies",
            "cover_image": None
        }

    # ==================== HELPER METHODS ====================
    
    def authenticate_admin(self):
        """Authenticate as admin user"""
        self.client.force_authenticate(user=self.admin)
    
    def authenticate_member(self, member=None):
        """Authenticate as member user"""
        if member is None:
            member = self.member
        self.client.force_authenticate(user=member)
    
    def authenticate_librarian(self):
        """Authenticate as librarian user"""
        self.client.force_authenticate(user=self.librarian)
    
    def create_book(self, payload=None, user=None):
        """Helper to create a book"""
        if payload is None:
            payload = self.book_payload
        if user is None:
            user = self.admin
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/books/", payload)
        if response.status_code != 201:
            print(f"BOOK CREATE ERROR: {response.data}")
        self.assertEqual(response.status_code, 201)
        return response.data
    
    def issue_book(self, book_id, user=None):
        """Helper to issue a book"""
        self.authenticate_member(user)
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data
    
    def return_book(self, transaction_id, user=None):
        """Helper to return a book"""
        self.authenticate_member(user)
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    # ==================== ISSUE BOOK TESTS ====================
    
    def test_issue_book_success(self):
        """Test successfully issuing a book"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"], book_data["id"])
        self.assertEqual(response.data["user"], self.member.id)
        self.assertEqual(response.data["status"], "ISSUED")
    
    def test_issue_book_decreases_available_copies(self):
        """Test issuing book decreases available copies"""
        book_data = self.create_book()
        initial_copies = book_data["available_copies"]
        
        self.authenticate_member()
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        # Check book availability
        book_response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(book_response.data["available_copies"], initial_copies - 1)
    
    def test_issue_unavailable_book_fails(self):
        """Test issuing unavailable book fails"""
        # Create book with 0 available copies
        self.authenticate_admin()
        book = self.book_payload.copy()
        book["available_copies"] = 0
        book["total_copies"] = 0
        response = self.client.post("/api/books/", book)
        book_id = response.data["id"]
        
        self.authenticate_member()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_issue_nonexistent_book_fails(self):
        """Test issuing non-existent book fails"""
        self.authenticate_member()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": 99999
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_issue_book_unauthenticated_fails(self):
        """Test unauthenticated user cannot issue book"""
        response = self.client.post("/api/transactions/issue/", {
            "book_id": 1
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_member_can_issue_multiple_books(self):
        """Test member can issue multiple different books"""
        book1 = self.create_book()
        book2 = self.create_book(self.book_payload_limited)
        
        self.authenticate_member()
        
        response1 = self.client.post("/api/transactions/issue/", {
            "book_id": book1["id"]
        })
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        response2 = self.client.post("/api/transactions/issue/", {
            "book_id": book2["id"]
        })
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    def test_issue_book_creates_transaction_record(self):
        """Test issuing book creates a transaction record"""
        book_data = self.create_book()
        self.authenticate_member()
        
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        transaction_id = response.data["id"]
        transaction = Transaction.objects.get(id=transaction_id)
        
        self.assertEqual(transaction.user, self.member)
        self.assertEqual(transaction.book.id, book_data["id"])
        self.assertEqual(transaction.status, "ISSUED")
        self.assertIsNotNone(transaction.issue_date)
        self.assertIsNotNone(transaction.due_date)
    
    def test_issue_book_sets_correct_due_date(self):
        """Test issuing book sets correct due date"""
        book_data = self.create_book()
        self.authenticate_member()
        
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        transaction = Transaction.objects.get(id=response.data["id"])
        expected_due_date = timezone.now().date() + timedelta(days=14)
        self.assertEqual(transaction.due_date, expected_due_date)

    # ==================== RETURN BOOK TESTS ====================
    
    def test_return_book_success(self):
        """Test successfully returning a book"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue the book first
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Return the book
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "RETURNED")
    
    def test_return_book_increases_available_copies(self):
        """Test returning book increases available copies"""
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Check book availability
        book_response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(book_response.data["available_copies"], 5)
    
    def test_return_already_returned_book_fails(self):
        """Test returning already returned book fails"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue and return
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Try to return again
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_return_nonexistent_transaction_fails(self):
        """Test returning non-existent transaction fails"""
        self.authenticate_member()
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": 99999
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_return_book_unauthenticated_fails(self):
        """Test unauthenticated user cannot return book"""
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": 1
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_return_book_sets_return_date(self):
        """Test returning book sets return date"""
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        return_response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        transaction = Transaction.objects.get(id=transaction_id)
        self.assertIsNotNone(transaction.return_date)
        self.assertEqual(transaction.status, "RETURNED")
    
    def test_return_overdue_book_sets_fine(self):
        """Test returning overdue book sets fine amount"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue a book
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Manually set due date to past to simulate overdue
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.due_date = timezone.now().date() - timedelta(days=5)
        transaction.save()
        
        # Return the book
        return_response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Reload transaction
        transaction.refresh_from_db()
        self.assertGreater(transaction.fine_amount, 0)
        # 5 days overdue * 5 per day = 25
        self.assertEqual(transaction.fine_amount, 25)

    # ==================== PAY FINE TESTS ====================
    
    def test_pay_fine_success(self):
        """Test paying fine for overdue book"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue and return (will have fine if overdue)
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Set overdue
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.due_date = timezone.now().date() - timedelta(days=3)
        transaction.save()
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Pay fine
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": transaction_id,
            "amount": 50
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 50)
    
    def test_pay_fine_creates_payment_record(self):
        """Test paying fine creates payment record"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue and return with fine
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.due_date = timezone.now().date() - timedelta(days=2)
        transaction.save()
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Pay fine
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": transaction_id,
            "amount": 50
        })
        
        payment_id = response.data["id"]
        payment = Payment.objects.get(id=payment_id)
        
        self.assertEqual(payment.amount, 50)
        self.assertEqual(payment.status, "SUCCESS")
        self.assertEqual(payment.transaction.id, transaction_id)
    
    def test_pay_fine_nonexistent_transaction_fails(self):
        """Test paying fine for non-existent transaction fails"""
        self.authenticate_member()
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": 99999,
            "amount": 50
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_pay_fine_unauthenticated_fails(self):
        """Test unauthenticated user cannot pay fine"""
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": 1,
            "amount": 50
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_pay_fine_for_returned_transaction_only(self):
        """Test can only pay fine for returned transactions"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue book (not returned yet)
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Try to pay fine before returning
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": transaction_id,
            "amount": 50
        })
        # Should fail because fine is 0 for non-overdue books
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==================== MY HISTORY TESTS ====================
    
    def test_my_history_success(self):
        """Test getting user's transaction history"""
        # Create and return a book
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": issue_response.data["id"]
        })
        
        # Get history
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_my_history_empty(self):
        """Test getting empty transaction history"""
        self.authenticate_member()
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_my_history_unauthenticated_fails(self):
        """Test unauthenticated user cannot access history"""
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_my_history_only_shows_own_transactions(self):
        """Test history only shows current user's transactions"""
        # Create transactions for both members
        book1 = self.create_book()
        book2 = self.create_book(self.book_payload_limited)
        
        # Member1 issues book1
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book1["id"]
        })
        
        # Member2 issues book2
        self.authenticate_member(self.member2)
        self.client.post("/api/transactions/issue/", {
            "book_id": book2["id"]
        })
        
        # Check Member1's history - should only show 1 transaction
        self.authenticate_member(self.member)
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"], book1["id"])
    
    def test_my_history_shows_issued_and_returned(self):
        """Test history shows both issued and returned books"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue a book
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        # Get history (book still issued)
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "ISSUED")
        
        # Return the book
        self.client.post("/api/transactions/return/", {
            "transaction_id": issue_response.data["id"]
        })
        
        # Get history (book now returned)
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "RETURNED")

    # ==================== ALL TRANSACTIONS (ADMIN) TESTS ====================
    
    def test_admin_can_view_all_transactions(self):
        """Test admin can view all transactions"""
        # Create some transactions with member
        book_data = self.create_book()
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.authenticate_admin()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_librarian_can_view_all_transactions(self):
        """Test librarian can view all transactions"""
        book_data = self.create_book()
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.authenticate_librarian()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_member_cannot_view_all_transactions(self):
        """Test member cannot view all transactions"""
        self.authenticate_member()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_view_all_transactions(self):
        """Test unauthenticated user cannot view all transactions"""
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_all_transactions_shows_all_users(self):
        """Test all transactions endpoint shows all users' transactions"""
        # Create transactions for multiple users
        book1 = self.create_book()
        book2 = self.create_book(self.book_payload_limited)
        
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book1["id"]
        })
        
        self.authenticate_member(self.member2)
        self.client.post("/api/transactions/issue/", {
            "book_id": book2["id"]
        })
        
        self.authenticate_admin()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(len(response.data), 2)

    # ==================== EDGE CASE TESTS ====================
    
    def test_user_cannot_return_other_users_transaction(self):
        """Test user cannot return another user's borrowed book"""
        book_data = self.create_book()
        
        # Member1 issues book
        self.authenticate_member(self.member)
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Member2 tries to return
        self.authenticate_member(self.member2)
        response = self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_cannot_pay_fine_for_other_users_transaction(self):
        """Test user cannot pay fine for another user's transaction"""
        book_data = self.create_book()
        
        # Member1 issues and returns book
        self.authenticate_member(self.member)
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Set overdue and return
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.due_date = timezone.now().date() - timedelta(days=1)
        transaction.save()
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Member2 tries to pay fine
        self.authenticate_member(self.member2)
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": transaction_id,
            "amount": 50
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_cannot_view_other_users_history(self):
        """Test user cannot view other users' history via API"""
        book_data = self.create_book()
        
        # Member1 issues book
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        # Login as Member2
        self.client.force_authenticate(user=self.member2)
        
        # Try to access Member1's transaction by ID
        # First get Member2's history (should be empty)
        response = self.client.get("/api/transactions/my-history/")
        self.assertEqual(len(response.data), 0)
    
    def test_concurrent_book_issues(self):
        """Test handling of concurrent book issues for limited copies"""
        # Create book with only 1 copy
        self.authenticate_admin()
        book = self.book_payload.copy()
        book["total_copies"] = 1
        book["available_copies"] = 1
        book_response = self.client.post("/api/books/", book)
        book_id = book_response.data["id"]
        
        # Both members try to issue at "same time"
        self.authenticate_member(self.member)
        response1 = self.client.post("/api/transactions/issue/", {
            "book_id": book_id
        })
        
        self.authenticate_member(self.member2)
        response2 = self.client.post("/api/transactions/issue/", {
            "book_id": book_id
        })
        
        # One should succeed, one should fail
        successful = [r for r in [response1, response2] if r.status_code == 201]
        failed = [r for r in [response1, response2] if r.status_code == 400]
        
        self.assertEqual(len(successful), 1)
        self.assertEqual(len(failed), 1)
    
    def test_issue_book_sets_correct_initial_fine(self):
        """Test issuing book sets initial fine to 0"""
        book_data = self.create_book()
        self.authenticate_member()
        
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        transaction = Transaction.objects.get(id=response.data["id"])
        self.assertEqual(transaction.fine_amount, 0)
    
    def test_return_book_zero_fine_for_on_time(self):
        """Test returning book on time has zero fine"""
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Return immediately (should be on time)
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        transaction = Transaction.objects.get(id=transaction_id)
        self.assertEqual(transaction.fine_amount, 0)
    
    def test_fine_calculation_accuracy(self):
        """Test fine calculation is accurate"""
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        transaction_id = issue_response.data["id"]
        
        # Set due date to 7 days ago
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.due_date = timezone.now().date() - timedelta(days=7)
        transaction.save()
        
        # Return the book
        self.client.post("/api/transactions/return/", {
            "transaction_id": transaction_id
        })
        
        # Fine should be 7 * 5 = 35
        transaction.refresh_from_db()
        self.assertEqual(transaction.fine_amount, 35)
    
    def test_transaction_history_response_format(self):
        """Test transaction history response format"""
        book_data = self.create_book()
        self.authenticate_member()
        
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        response = self.client.get("/api/transactions/my-history/")
        
        self.assertIsInstance(response.data, list)
        if len(response.data) > 0:
            transaction = response.data[0]
            self.assertIn("id", transaction)
            self.assertIn("book", transaction)
            self.assertIn("user", transaction)
            self.assertIn("status", transaction)
            self.assertIn("issue_date", transaction)
            self.assertIn("due_date", transaction)
    
    def test_all_transactions_response_format(self):
        """Test all transactions response format for admin"""
        book_data = self.create_book()
        self.authenticate_member()
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.authenticate_admin()
        response = self.client.get("/api/transactions/all/")
        
        self.assertIsInstance(response.data, list)
        if len(response.data) > 0:
            transaction = response.data[0]
            self.assertIn("id", transaction)
            self.assertIn("book", transaction)
            self.assertIn("user", transaction)
            self.assertIn("status", transaction)
    
    def test_admin_can_issue_book(self):
        """Test admin can issue books"""
        book_data = self.create_book()
        
        self.authenticate_admin()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_librarian_can_issue_book(self):
        """Test librarian can issue books"""
        book_data = self.create_book()
        
        self.authenticate_librarian()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_issue_and_immediate_return(self):
        """Test issuing and immediately returning a book"""
        book_data = self.create_book()
        self.authenticate_member()
        
        # Issue
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        self.assertEqual(issue_response.status_code, status.HTTP_201_CREATED)
        
        # Return
        return_response = self.client.post("/api/transactions/return/", {
            "transaction_id": issue_response.data["id"]
        })
        self.assertEqual(return_response.status_code, status.HTTP_200_OK)
        
        # Verify transaction is returned
        transaction = Transaction.objects.get(id=issue_response.data["id"])
        self.assertEqual(transaction.status, "RETURNED")
        self.assertIsNotNone(transaction.return_date)

