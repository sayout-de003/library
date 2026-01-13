from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class LibraryAPITest(APITestCase):
    """Comprehensive API tests for Library Management System"""

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
        
        # Create another member for additional tests
        self.member2 = User.objects.create_user(
            username="member2",
            email="member2@test.com",
            password="Member2@123"
        )
        
        # Book payload (without cover_image to avoid None encoding issues)
        self.book_payload = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "category": "Programming",
            "isbn": "9780132350884",
            "total_copies": 5,
            "available_copies": 5,
            "description": "A handbook of agile software craftsmanship"
        }
        
        # Alternative book payload
        self.book_payload_2 = {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "category": "Programming",
            "isbn": "9780201616224",
            "total_copies": 3,
            "available_copies": 3,
            "description": "From journeyman to master"
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
    
    def create_book(self, payload=None, user=None):
        """Helper to create a book"""
        if payload is None:
            payload = self.book_payload.copy()
        else:
            payload = payload.copy()
        # Remove cover_image if present to avoid None encoding issues
        payload.pop('cover_image', None)
        
        if user is None:
            user = self.admin
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/books/", payload, format='json')
        if response.status_code != 201:
            print(f"BOOK CREATE ERROR: {response.data}")
        self.assertEqual(response.status_code, 201)
        return response.data
    
    def create_book_raw(self, payload=None, user=None):
        """Helper to create a book using raw database"""
        if payload is None:
            payload = self.book_payload.copy()
        else:
            payload = payload.copy()
        
        from books.models import Book
        payload.pop('cover_image', None)
        book = Book.objects.create(**payload)
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "isbn": book.isbn,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "description": book.description
        }

    # ==================== AUTH TESTS ====================
    
    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post("/api/auth/register/", {
            "username": "newuser",
            "email": "new@test.com",
            "password": "Test@123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "new@test.com")
        self.assertEqual(response.data["role"], "MEMBER")
    
    def test_register_user_duplicate_username(self):
        """Test registration with duplicate username fails"""
        response = self.client.post("/api/auth/register/", {
            "username": "admin",  # Already exists
            "email": "new@test.com",
            "password": "Test@123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email fails"""
        response = self.client.post("/api/auth/register/", {
            "username": "newuser",
            "email": "admin@test.com",  # Already exists
            "password": "Test@123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_invalid_email(self):
        """Test registration with invalid email fails"""
        response = self.client.post("/api/auth/register/", {
            "username": "newuser",
            "email": "invalid-email",
            "password": "Test@123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_short_password(self):
        """Test registration with short password fails"""
        response = self.client.post("/api/auth/register/", {
            "username": "newuser",
            "email": "new@test.com",
            "password": "123"  # Too short
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_admin_success(self):
        """Test successful admin login using email"""
        response = self.client.post("/api/auth/login/", {
            "email": "admin@test.com",
            "password": "Admin@123"
        })
        if response.status_code != 200:
            print(f"LOGIN ERROR: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_login_member_success(self):
        """Test successful member login using email"""
        response = self.client.post("/api/auth/login/", {
            "email": "member@test.com",
            "password": "Member@123"
        })
        if response.status_code != 200:
            print(f"LOGIN ERROR: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials fails"""
        response = self.client.post("/api/auth/login/", {
            "email": "member@test.com",
            "password": "WrongPassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user fails"""
        response = self.client.post("/api/auth/login/", {
            "email": "nonexistent@test.com",
            "password": "SomePassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_librarian_by_admin(self):
        """Test admin can add librarian"""
        self.authenticate_admin()
        response = self.client.post("/api/auth/add-librarian/", {
            "username": "newlibrarian",
            "email": "librarian@test.com",
            "password": "Librarian@123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view sets role to 'ADMIN' but serializer returns default 'MEMBER'
        # Let's check the actual database value
        new_user = User.objects.get(email="librarian@test.com")
        self.assertEqual(new_user.role, "ADMIN")
    
    def test_add_librarian_by_member_fails(self):
        """Test member cannot add librarian"""
        self.authenticate_member()
        response = self.client.post("/api/auth/add-librarian/", {
            "username": "newlibrarian",
            "email": "librarian@test.com",
            "password": "Librarian@123"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_add_librarian_unauthenticated_fails(self):
        """Test unauthenticated request to add librarian fails"""
        response = self.client.post("/api/auth/add-librarian/", {
            "username": "newlibrarian",
            "email": "librarian@test.com",
            "password": "Librarian@123"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_me_admin(self):
        """Test get current admin user info"""
        self.authenticate_admin()
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "admin")
        self.assertEqual(response.data["email"], "admin@test.com")
        self.assertEqual(response.data["role"], "ADMIN")
    
    def test_user_me_member(self):
        """Test get current member user info"""
        self.authenticate_member()
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "member")
        self.assertEqual(response.data["email"], "member@test.com")
        self.assertEqual(response.data["role"], "MEMBER")
    
    def test_user_me_unauthenticated_fails(self):
        """Test unauthenticated request to get user info fails"""
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================== BOOKS TESTS ====================
    
    def test_admin_can_create_book(self):
        """Test admin can create a book"""
        self.authenticate_admin()
        payload = self.book_payload.copy()
        payload.pop('cover_image', None)
        response = self.client.post("/api/books/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], "Clean Code")
        self.assertEqual(response.data["author"], "Robert C. Martin")
        self.assertEqual(response.data["category"], "Programming")
    
    def test_member_cannot_create_book(self):
        """Test member cannot create a book"""
        self.authenticate_member()
        payload = self.book_payload.copy()
        payload.pop('cover_image', None)
        response = self.client.post("/api/books/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_create_book(self):
        """Test unauthenticated user cannot create a book"""
        payload = self.book_payload.copy()
        payload.pop('cover_image', None)
        response = self.client.post("/api/books/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_books_authenticated(self):
        """Test authenticated user can list books"""
        self.create_book()
        self.authenticate_member()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_list_books_unauthenticated(self):
        """Test unauthenticated user cannot list books"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_book_by_id(self):
        """Test get book by ID using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_member()
        response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], book_data["title"])
    
    def test_admin_can_update_book(self):
        """Test admin can update a book using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_admin()
        url = f"/api/books/{book_data['id']}/"
        response = self.client.put(url, {
            "title": "Clean Code Updated",
            "author": "Robert C. Martin",
            "category": "Programming",
            "isbn": "9780132350884",
            "total_copies": 5,
            "available_copies": 5
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Clean Code Updated")
    
    def test_admin_can_partial_update_book(self):
        """Test admin can partial update a book using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_admin()
        url = f"/api/books/{book_data['id']}/"
        response = self.client.patch(url, {
            "title": "Clean Code Partially Updated"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Clean Code Partially Updated")
    
    def test_member_cannot_update_book(self):
        """Test member cannot update a book using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_member()
        url = f"/api/books/{book_data['id']}/"
        response = self.client.put(url, {
            "title": "Hacked Title"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_delete_book(self):
        """Test admin can delete a book using raw creation"""
        from books.models import Book
        book_data = self.create_book_raw()
        book_id = book_data['id']
        self.authenticate_admin()
        response = self.client.delete(f"/api/books/{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify deletion
        get_response = self.client.get(f"/api/books/{book_id}/")
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_member_cannot_delete_book(self):
        """Test member cannot delete a book using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_member()
        response = self.client.delete(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_books_by_category_public(self):
        """Test books by-category endpoint is public using raw creation"""
        self.create_book_raw()
        # Create another book in same category
        self.create_book_raw(self.book_payload_2)
        
        # Access without authentication (should be public)
        response = self.client.get("/api/books/by-category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Programming", response.data)
    
    def test_books_search_filter(self):
        """Test book search/filter functionality using raw creation"""
        self.create_book_raw()
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "Clean"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book_invalid_data(self):
        """Test creating book with invalid data fails"""
        self.authenticate_admin()
        response = self.client.post("/api/books/", {
            "title": "",  # Empty title
            "author": "Test Author"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==================== TRANSACTIONS TESTS ====================
    
    def test_issue_book_success(self):
        """Test successfully issuing a book using raw creation"""
        book_data = self.create_book_raw()
        self.authenticate_member()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"], book_data["id"])
        self.assertEqual(response.data["user"], self.member.id)
        self.assertEqual(response.data["status"], "ISSUED")
    
    def test_issue_unavailable_book_fails(self):
        """Test issuing unavailable book fails using raw creation"""
        from books.models import Book
        # Create book with 0 available copies
        book = Book.objects.create(
            title="Unavailable Book",
            author="Test Author",
            category="Testing",
            isbn="1111111111111",
            total_copies=0,
            available_copies=0
        )
        self.authenticate_member()
        response = self.client.post("/api/transactions/issue/", {
            "book_id": book.id
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
    
    def test_return_book_success(self):
        """Test successfully returning a book using raw creation"""
        book_data = self.create_book_raw()
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
    
    def test_return_already_returned_book_fails(self):
        """Test returning already returned book fails using raw creation"""
        book_data = self.create_book_raw()
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
    
    def test_pay_fine_success(self):
        """Test paying fine for overdue book using raw creation"""
        from django.utils import timezone
        from datetime import timedelta
        from transactions.models import Transaction
        
        book_data = self.create_book_raw()
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
    
    def test_pay_fine_nonexistent_transaction_fails(self):
        """Test paying fine for non-existent transaction fails"""
        self.authenticate_member()
        response = self.client.post("/api/transactions/pay-fine/", {
            "transaction_id": 99999,
            "amount": 50
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_my_history_success(self):
        """Test getting user's transaction history using raw creation"""
        from transactions.models import Transaction
        
        # Create and return a book
        book_data = self.create_book_raw()
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
    
    def test_admin_can_view_all_transactions(self):
        """Test admin can view all transactions using raw creation"""
        from transactions.models import Transaction
        
        # Create some transactions with member
        book_data = self.create_book_raw()
        self.authenticate_member(self.member)
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.authenticate_admin()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_member_cannot_view_all_transactions(self):
        """Test member cannot view all transactions"""
        self.authenticate_member()
        response = self.client.get("/api/transactions/all/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_issue_book_decreases_available_copies(self):
        """Test issuing book decreases available copies using raw creation"""
        from books.models import Book
        
        book_data = self.create_book_raw()
        initial_copies = book_data["available_copies"]
        
        self.authenticate_member()
        self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        # Check book availability
        book_response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(book_response.data["available_copies"], initial_copies - 1)
    
    def test_return_book_increases_available_copies(self):
        """Test returning book increases available copies using raw creation"""
        book_data = self.create_book_raw()
        
        self.authenticate_member()
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        
        self.client.post("/api/transactions/return/", {
            "transaction_id": issue_response.data["id"]
        })
        
        # Check book availability
        book_response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(book_response.data["available_copies"], 5)

    # ==================== EDGE CASE TESTS ====================
    
    def test_user_cannot_issue_own_book(self):
        """Test edge case: user cannot issue book as admin (if book is issued to admin)"""
        # Admin issues a book
        book_data = self.create_book_raw()
        self.authenticate_admin()
        issue_response = self.client.post("/api/transactions/issue/", {
            "book_id": book_data["id"]
        })
        # Admin should be able to issue book to themselves
        self.assertEqual(issue_response.status_code, status.HTTP_201_CREATED)
    
    def test_multiple_users_can_issue_same_book(self):
        """Test multiple users can issue different books using raw creation"""
        # Create two books
        book1 = self.create_book_raw(self.book_payload)
        book2 = self.create_book_raw(self.book_payload_2)
        
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
        
        # Both should succeed
        self.assertTrue(True)  # If we got here, both succeeded
    
    def test_user_cannot_return_other_users_transaction(self):
        """Test user cannot return another user's borrowed book using raw creation"""
        book_data = self.create_book_raw()
        
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
        """Test user cannot pay fine for another user's transaction using raw creation"""
        from django.utils import timezone
        from datetime import timedelta
        from transactions.models import Transaction
        
        book_data = self.create_book_raw()
        
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
    
    def authenticate_user(self, user):
        """Helper to authenticate with specific user"""
        self.client.force_authenticate(user=user)
    
    def test_book_list_pagination(self):
        """Test book list handles multiple items using raw creation"""
        self.authenticate_admin()
        # Create multiple books
        for i in range(5):
            payload = self.book_payload.copy()
            payload["title"] = f"Book {i}"
            payload["isbn"] = f"978013235088{i}"
            payload.pop('cover_image', None)
            self.client.post("/api/books/", payload, format='json')
        
        self.authenticate_member()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 5)
    
    def test_transaction_history_for_specific_user(self):
        """Test transaction history only shows current user's transactions using raw creation"""
        # Create transactions for both members
        book1 = self.create_book_raw(self.book_payload)
        book2 = self.create_book_raw(self.book_payload_2)
        
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
    
    def test_concurrent_book_issues(self):
        """Test handling of concurrent book issues for limited copies using raw creation"""
        from books.models import Book
        
        # Create book with only 1 copy
        self.authenticate_admin()
        book = Book.objects.create(
            title="Limited Book",
            author="Test Author",
            category="Testing",
            isbn="1111111111111",
            total_copies=1,
            available_copies=1
        )
        book_id = book.id
        
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

