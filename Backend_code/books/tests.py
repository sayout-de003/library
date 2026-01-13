from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book

User = get_user_model()


class BookAPITest(APITestCase):
    """Comprehensive tests for Book API"""

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
        
        # Sample book payloads
        self.book_payload_1 = {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "category": "Programming",
            "isbn": "9780132350884",
            "total_copies": 5,
            "available_copies": 5,
            "description": "A handbook of agile software craftsmanship",
            "cover_image": None
        }
        
        self.book_payload_2 = {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "category": "Programming",
            "isbn": "9780201616224",
            "total_copies": 3,
            "available_copies": 3,
            "description": "From journeyman to master",
            "cover_image": None
        }
        
        self.book_payload_3 = {
            "title": "Design Patterns",
            "author": "Erich Gamma",
            "category": "Software Engineering",
            "isbn": "9780201633610",
            "total_copies": 2,
            "available_copies": 2,
            "description": "Elements of reusable object-oriented software",
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
    
    def create_book(self, payload=None, user=None):
        """Helper to create a book"""
        if payload is None:
            payload = self.book_payload_1
        if user is None:
            user = self.admin
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/books/", payload)
        if response.status_code != 201:
            print(f"BOOK CREATE ERROR: {response.data}")
        self.assertEqual(response.status_code, 201)
        return response.data

    # ==================== CREATE BOOK TESTS ====================
    
    def test_admin_can_create_book(self):
        """Test admin can create a book"""
        self.authenticate_admin()
        response = self.client.post("/api/books/", self.book_payload_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], "Clean Code")
        self.assertEqual(response.data["author"], "Robert C. Martin")
        self.assertEqual(response.data["category"], "Programming")
        self.assertEqual(response.data["total_copies"], 5)
        self.assertEqual(response.data["available_copies"], 5)
    
    def test_admin_can_create_multiple_books(self):
        """Test admin can create multiple books"""
        self.authenticate_admin()
        
        response1 = self.client.post("/api/books/", self.book_payload_1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        response2 = self.client.post("/api/books/", self.book_payload_2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        response3 = self.client.post("/api/books/", self.book_payload_3)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        
        # Verify all books exist
        list_response = self.client.get("/api/books/")
        self.assertEqual(len(list_response.data), 3)
    
    def test_member_cannot_create_book(self):
        """Test member cannot create a book"""
        self.authenticate_member()
        response = self.client.post("/api/books/", self.book_payload_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_create_book(self):
        """Test unauthenticated user cannot create a book"""
        response = self.client.post("/api/books/", self.book_payload_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_with_empty_title(self):
        """Test creating book with empty title fails"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["title"] = ""
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_with_empty_author(self):
        """Test creating book with empty author fails"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["author"] = ""
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_with_negative_copies(self):
        """Test creating book with negative copies fails"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["total_copies"] = -1
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_with_more_available_than_total(self):
        """Test creating book with available > total fails"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["total_copies"] = 5
        payload["available_copies"] = 10
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_book_without_isbn(self):
        """Test creating book without ISBN"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        del payload["isbn"]
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_with_duplicate_isbn(self):
        """Test creating book with duplicate ISBN"""
        self.authenticate_admin()
        self.client.post("/api/books/", self.book_payload_1)
        
        payload2 = self.book_payload_2.copy()
        payload2["isbn"] = self.book_payload_1["isbn"]  # Same ISBN
        response = self.client.post("/api/books/", payload2)
        # Should succeed (no unique constraint on ISBN)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ==================== LIST BOOKS TESTS ====================
    
    def test_list_books_authenticated(self):
        """Test authenticated user can list books"""
        self.create_book()
        self.create_book(self.book_payload_2)
        
        self.authenticate_member()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
    
    def test_list_books_unauthenticated(self):
        """Test unauthenticated user cannot list books"""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_empty_books(self):
        """Test listing empty books"""
        self.authenticate_member()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_list_books_ordering(self):
        """Test books are listed in expected order"""
        self.create_book(self.book_payload_2)
        self.create_book(self.book_payload_1)
        self.create_book(self.book_payload_3)
        
        self.authenticate_member()
        response = self.client.get("/api/books/")
        # Assuming default ordering is by title
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    # ==================== RETRIEVE BOOK TESTS ====================
    
    def test_get_book_by_id(self):
        """Test get book by ID"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], book_data["title"])
        self.assertEqual(response.data["author"], book_data["author"])
    
    def test_get_nonexistent_book(self):
        """Test get non-existent book returns 404"""
        self.authenticate_member()
        response = self.client.get("/api/books/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_book_includes_all_fields(self):
        """Test get book returns all fields"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.data["title"], "Clean Code")
        self.assertEqual(response.data["author"], "Robert C. Martin")
        self.assertEqual(response.data["category"], "Programming")
        self.assertEqual(response.data["isbn"], "9780132350884")
        self.assertEqual(response.data["total_copies"], 5)
        self.assertEqual(response.data["available_copies"], 5)

    # ==================== UPDATE BOOK TESTS ====================
    
    def test_admin_can_update_book(self):
        """Test admin can update a book"""
        book_data = self.create_book()
        self.authenticate_admin()
        response = self.client.put(f"/api/books/{book_data['id']}/", {
            "title": "Clean Code Updated",
            "author": "Robert C. Martin",
            "category": "Programming",
            "isbn": "9780132350884",
            "total_copies": 10,
            "available_copies": 10,
            "description": "Updated description"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Clean Code Updated")
        self.assertEqual(response.data["total_copies"], 10)
    
    def test_admin_can_partial_update_book(self):
        """Test admin can partial update a book"""
        book_data = self.create_book()
        self.authenticate_admin()
        response = self.client.patch(f"/api/books/{book_data['id']}/", {
            "title": "Clean Code Partially Updated"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Clean Code Partially Updated")
        # Other fields should remain unchanged
        self.assertEqual(response.data["author"], "Robert C. Martin")
    
    def test_member_cannot_update_book(self):
        """Test member cannot update a book"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.put(f"/api/books/{book_data['id']}/", {
            "title": "Hacked Title"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_member_cannot_partial_update_book(self):
        """Test member cannot partial update a book"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.patch(f"/api/books/{book_data['id']}/", {
            "title": "Hacked Title"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_update_book(self):
        """Test unauthenticated user cannot update a book"""
        book_data = self.create_book()
        response = self.client.put(f"/api/books/{book_data['id']}/", {
            "title": "Hacked Title"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_nonexistent_book(self):
        """Test updating non-existent book returns 404"""
        self.authenticate_admin()
        response = self.client.put("/api/books/99999/", {
            "title": "Updated Title"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== DELETE BOOK TESTS ====================
    
    def test_admin_can_delete_book(self):
        """Test admin can delete a book"""
        book_data = self.create_book()
        self.authenticate_admin()
        response = self.client.delete(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify deletion
        get_response = self.client.get(f"/api/books/{book_data['id']}/")
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_member_cannot_delete_book(self):
        """Test member cannot delete a book"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.delete(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_cannot_delete_book(self):
        """Test unauthenticated user cannot delete a book"""
        book_data = self.create_book()
        response = self.client.delete(f"/api/books/{book_data['id']}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_nonexistent_book(self):
        """Test deleting non-existent book returns 404"""
        self.authenticate_admin()
        response = self.client.delete("/api/books/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_book_removes_from_database(self):
        """Test deleting book removes it from database"""
        book_data = self.create_book()
        book_id = book_data["id"]
        
        self.authenticate_admin()
        self.client.delete(f"/api/books/{book_id}/")
        
        # Verify book is deleted
        self.assertFalse(Book.objects.filter(id=book_id).exists())

    # ==================== BY CATEGORY TESTS ====================
    
    def test_books_by_category_public(self):
        """Test books by-category endpoint is public"""
        self.create_book()
        self.create_book(self.book_payload_2)
        self.create_book(self.book_payload_3)
        
        # Access without authentication (should be public)
        response = self.client.get("/api/books/by-category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check structure
        self.assertIn("Programming", response.data)
        self.assertIn("Software Engineering", response.data)
    
    def test_books_by_category_structure(self):
        """Test books by-category returns correct structure"""
        self.create_book()
        
        response = self.client.get("/api/books/by-category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that programming category exists
        self.assertIn("Programming", response.data)
        
        # Check books in category
        programming_books = response.data["Programming"]
        self.assertIsInstance(programming_books, list)
        self.assertGreater(len(programming_books), 0)
        
        # Check book structure
        book = programming_books[0]
        self.assertIn("id", book)
        self.assertIn("title", book)
        self.assertIn("author", book)
    
    def test_books_by_category_empty_category(self):
        """Test books by-category with empty category"""
        self.authenticate_admin()
        # Create book without category
        payload = self.book_payload_1.copy()
        payload["category"] = ""
        self.client.post("/api/books/", payload)
        
        # Check for "Uncategorized"
        response = self.client.get("/api/books/by-category/")
        self.assertIn("Uncategorized", response.data)
    
    def test_books_by_category_with_no_books(self):
        """Test books by-category with no books"""
        response = self.client.get("/api/books/by-category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ==================== SEARCH/FILTER TESTS ====================
    
    def test_books_search_by_title(self):
        """Test book search by title"""
        self.create_book()
        self.create_book(self.book_payload_2)
        
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "Clean"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find "Clean Code"
        titles = [book["title"] for book in response.data]
        self.assertTrue(any("Clean" in title for title in titles))
    
    def test_books_search_by_author(self):
        """Test book search by author"""
        self.create_book()
        self.create_book(self.book_payload_2)
        
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "Robert"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find "Clean Code" by Robert C. Martin
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Robert C. Martin")
    
    def test_books_search_by_category(self):
        """Test book search by category"""
        self.create_book()
        self.create_book(self.book_payload_3)
        
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "Programming"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find books in Programming category
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_books_search_no_results(self):
        """Test book search with no results"""
        self.create_book()
        
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "Nonexistent Book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_books_search_case_insensitive(self):
        """Test book search is case insensitive"""
        self.create_book()
        
        self.authenticate_member()
        response = self.client.get("/api/books/", {"search": "clean code"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ==================== EDGE CASE TESTS ====================
    
    def test_update_book_availability_only(self):
        """Test admin can update only availability"""
        book_data = self.create_book()
        self.authenticate_admin()
        
        # Simulate issuing a book (update available copies)
        response = self.client.patch(f"/api/books/{book_data['id']}/", {
            "available_copies": 4
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["available_copies"], 4)
    
    def test_create_book_special_characters_in_title(self):
        """Test creating book with special characters in title"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["title"] = "Clean Code: A Handbook of Agile Software Craftsmanship (2nd Edition)"
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
    
    def test_create_book_unicode_characters(self):
        """Test creating book with unicode characters"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["title"] = "编程艺术"
        payload["author"] = "张三"
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_book_long_description(self):
        """Test creating book with long description"""
        self.authenticate_admin()
        payload = self.book_payload_1.copy()
        payload["description"] = "A" * 1000  # 1000 character description
        response = self.client.post("/api/books/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["description"]), 1000)
    
    def test_admin_can_update_book_to_zero_copies(self):
        """Test admin can update book to have zero copies"""
        book_data = self.create_book()
        self.authenticate_admin()
        response = self.client.patch(f"/api/books/{book_data['id']}/", {
            "available_copies": 0,
            "total_copies": 0
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["available_copies"], 0)
    
    def test_books_list_response_format(self):
        """Test books list response format"""
        self.create_book()
        self.authenticate_member()
        response = self.client.get("/api/books/")
        
        # Should return a list
        self.assertIsInstance(response.data, list)
        
        # Each book should have required fields
        if len(response.data) > 0:
            book = response.data[0]
            self.assertIn("id", book)
            self.assertIn("title", book)
            self.assertIn("author", book)
            self.assertIn("category", book)
            self.assertIn("available_copies", book)
    
    def test_books_detail_response_format(self):
        """Test books detail response format"""
        book_data = self.create_book()
        self.authenticate_member()
        response = self.client.get(f"/api/books/{book_data['id']}/")
        
        # Should return a dict with all fields
        self.assertIsInstance(response.data, dict)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("author", response.data)
        self.assertIn("category", response.data)
        self.assertIn("isbn", response.data)
        self.assertIn("total_copies", response.data)
        self.assertIn("available_copies", response.data)
        self.assertIn("description", response.data)

