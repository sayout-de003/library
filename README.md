# 📚 Library Management System

A full-stack Library Management System built with **Django REST Framework** (backend) and **React 19 + Vite** (frontend). This system provides comprehensive library operations including book management, user authentication, book issuing/returning, and fine payments.

![Library Management System](https://via.placeholder.com/1200x400?text=Library+Management+System)

---

## 🏗️ Project Structure

```
library_asg/
├── Backend_code/                 # Django Backend
│   ├── backend/                  # Django Project Settings
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuration settings
│   │   ├── urls.py              # Main URL routing
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── books/                    # Book Management App
│   │   ├── models.py            # Book model
│   │   ├── views.py             # Book API views
│   │   ├── serializers.py       # DRF Serializers
│   │   ├── urls.py              # Book endpoints
│   │   ├── admin.py
│   │   └── migrations/
│   ├── users/                    # User Management App
│   │   ├── models.py            # Custom User model
│   │   ├── views.py             # User API views
│   │   ├── serializers.py       # User serializers
│   │   ├── urls.py              # Auth endpoints
│   │   ├── admin.py
│   │   └── migrations/
│   ├── transactions/             # Transaction Management App
│   │   ├── models.py            # Transaction & Payment models
│   │   ├── views.py             # Transaction API views
│   │   ├── serializers.py       # Transaction serializers
│   │   ├── urls.py              # Transaction endpoints
│   │   ├── signals.py
│   │   ├── admin.py
│   │   └── migrations/
│   ├── scripts/                  # Utility Scripts
│   │   ├── seed_books.py        # Seed 100 demo books
│   │   └── seed_demo.py
│   ├── covers/                   # Book cover images
│   ├── media/                    # Uploaded files
│   └── manage.py                 # Django management script
│
├── Frontend_code/                # React Frontend
│   └── frontend/                 # Vite React App
│       ├── src/
│       │   ├── components/       # Reusable UI Components
│       │   │   ├── Navbar.jsx
│       │   │   ├── Footer.jsx
│       │   │   ├── Button.jsx
│       │   │   └── ProtectedRoute.jsx
│       │   ├── pages/            # Page Components
│       │   │   ├── Landing/
│       │   │   │   └── Home.jsx
│       │   │   ├── Auth/
│       │   │   │   ├── Login.jsx
│       │   │   │   └── Register.jsx
│       │   │   ├── Member/
│       │   │   │   ├── MemberDashboard.jsx
│       │   │   │   ├── SearchBooks.jsx
│       │   │   │   ├── BookReader.jsx
│       │   │   │   └── Payment.jsx
│       │   │   └── Admin/
│       │   │       ├── AdminDashboard.jsx
│       │   │       ├── ManageBooks.jsx
│       │   │       └── AddLibrarian.jsx
│       │   ├── context/          # React Context
│       │   │   └── AuthContext.jsx
│       │   ├── services/         # API Services
│       │   │   └── api.js
│       │   ├── App.jsx           # Main App Component
│       │   ├── main.jsx          # Entry Point
│       │   └── index.css         # Global Styles
│       ├── index.html
│       ├── package.json
│       ├── vite.config.js
│       ├── tailwind.config.js
│       └── eslint.config.js
│
└── README.md                      # This file
```

---

## 🚀 Features

### 👨‍💼 Admin Features
- **Dashboard**: View statistics (total books, users, transactions)
- **Manage Books**: Add, edit, delete books with cover images and PDFs
- **Add Librarians**: Create new librarian/admin accounts
- **View All Transactions**: Monitor all book issues and returns

### 👤 Member Features
- **Dashboard**: View borrowed books and history
- **Search Books**: Search by title, author, or category
- **Issue Books**: Borrow available books
- **Read Books**: Built-in PDF reader for borrowed books
- **Pay Fines**: Pay overdue fines online
- **Return Books**: Return borrowed books

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based auth
- **Role-Based Access Control**: Admin and Member roles
- **Protected Routes**: Only authorized users can access specific pages

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 6.0** | Web Framework |
| **Django REST Framework** | REST API |
| **SQLite** | Database |
| **SimpleJWT** | JWT Authentication |
| **CORS Headers** | Cross-Origin Resource Sharing |
| **Pillow** | Image Processing |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI Library |
| **Vite** | Build Tool |
| **Tailwind CSS** | Styling |
| **React Router DOM** | Routing |
| **Axios** | HTTP Client |
| **Framer Motion** | Animations |
| **React-PDF** | PDF Viewer |
| **Recharts** | Charts & Analytics |
| **Lucide React** | Icons |

---

## 📡 API Endpoints

### Authentication (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new member | No |
| POST | `/api/auth/login/` | Login (get tokens) | No |
| POST | `/api/auth/refresh/` | Refresh access token | No |
| GET | `/api/auth/me/` | Get current user | Yes |
| POST | `/api/auth/add-librarian/` | Add new librarian | Admin |
| GET | `/api/auth/count/` | Get user count | Admin |

### Books (`/api/books/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/books/` | List all books | Yes |
| POST | `/api/books/` | Create book | Admin |
| GET | `/api/books/{id}/` | Book details | Yes |
| PUT | `/api/books/{id}/` | Update book | Admin |
| DELETE | `/api/books/{id}/` | Delete book | Admin |
| GET | `/api/books/by-category/` | Group books by category | No |
| GET | `/api/books/count/` | Get total book count | Yes |

### Transactions (`/api/transactions/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/transactions/issue/` | Issue a book | Yes |
| POST | `/api/transactions/return/` | Return a book | Yes |
| GET | `/api/transactions/my-history/` | Member's transaction history | Yes |
| POST | `/api/transactions/pay-fine/` | Pay fine | Yes |
| GET | `/api/transactions/all/` | All transactions (admin) | Admin |

---

## 💻 System Requirements

- **Python 3.8+**
- **Node.js 18+**
- **npm or yarn**
- **Git**

---

## 🧑‍💻 Installation Guide

### Step 1: Clone the Repository

```bash
cd /Users/sayantande/library_asg
```

### Step 2: Backend Setup (Django)

#### 2.1 Create Virtual Environment

```bash
cd Backend_code
python -m venv venv
```

#### 2.2 Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### 2.3 Install Python Dependencies

```bash
pip install django djangorestframework django-cors-headers pillow djangorestframework-simplejwt
```

#### 2.4 Run Database Migrations

```bash
python manage.py migrate
```

#### 2.5 Seed Demo Books (Optional)

```bash
python scripts/seed_books.py
```

This will add 100 books across 6 categories:
- Technology (20 books)
- Science Fiction (15 books)
- Fantasy (15 books)
- Classics (15 books)
- Mystery & Thriller (15 books)
- History & Biography (10 books)
- Finance (10 books)

#### 2.6 Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### 2.7 Start Django Server

```bash
python manage.py runserver
```

The backend will run at: **http://localhost:8000**

---

### Step 3: Frontend Setup (React)

#### 3.1 Open New Terminal

#### 3.2 Navigate to Frontend Directory

```bash
cd /Users/sayantande/library_asg/Frontend_code/frontend
```

#### 3.3 Install Node Dependencies

```bash
npm install
```

#### 3.4 Start Development Server

```bash
npm run dev
```

The frontend will run at: **http://localhost:5173**

---

## 🎮 How to Use

### Access the Application

1. Open your browser and go to: **http://localhost:5173**
2. You'll see the landing page with login/register options

### Create Admin Account

1. Go to: **http://localhost:8000/admin/**
2. Login with the superuser you created
3. Create additional librarians if needed

### Member Registration

1. Click "Register" on the home page
2. Fill in the registration form
3. You'll be assigned the "MEMBER" role by default

### Workflow

#### For Members:
1. **Login** with your credentials
2. **Search** for books using the search bar
3. **Click "Issue"** on available books
4. **Go to Dashboard** to view borrowed books
5. **Click "Read"** to open the PDF reader
6. **Return** books before the due date
7. **Pay fines** if you return late

#### For Admins:
1. **Login** with admin credentials
2. **Manage Books**: Add new books with cover images and PDFs
3. **Add Librarians**: Create new admin accounts
4. **View Dashboard**: See system statistics
5. **Monitor Transactions**: Track all book issues and returns

---

## 🔧 Database Configuration

By default, the project uses **SQLite**. However, you can easily switch to **PostgreSQL** or **MongoDB** for production environments.

---

### Option 1: Using PostgreSQL (Recommended for Production)

PostgreSQL is a powerful, open-source relational database that's perfect for production environments.

#### Step 1: Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

#### Step 2: Create Database and User

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE library_db;
CREATE USER library_user WITH PASSWORD 'your_secure_password';
ALTER ROLE library_user SET client_encoding TO 'utf8';
ALTER ROLE library_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_user;
\q
```

#### Step 3: Install PostgreSQL Python Driver

```bash
pip install psycopg2-binary
```

#### Step 4: Update Django Settings

Edit `Backend_code/backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'library_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Step 5: Run Migrations

```bash
python manage.py migrate
```

---

### Option 2: Using MongoDB (NoSQL Approach)

MongoDB is a document-based NoSQL database. For Django, we'll use `djongo` as the ORM.

#### Step 1: Install MongoDB

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Windows:**
Download from https://www.mongodb.com/try/download/community

#### Step 2: Create Database

```bash
mongosh
```

```javascript
use library_db
db.createUser({
  user: "library_admin",
  pwd: "your_secure_password",
  roles: [{ role: "readWrite", db: "library_db" }]
})
```

#### Step 3: Install MongoDB Python Driver

```bash
pip install djongo pymongo
```

#### Step 4: Update Django Settings

Edit `Backend_code/backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'library_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb://library_admin:your_secure_password@localhost:27017/library_db?authSource=admin',
            'retryWrites': True,
            'w': 'majority',
        },
    }
}
```

#### Step 5: Run Migrations

```bash
python manage.py migrate
```

> ⚠️ **Note**: Djongo creates collections automatically. Some Django features like `migrate --fake` may not work as expected.

---

### Environment Variables (Recommended)

Create a `.env` file in `Backend_code/` to manage sensitive configurations:

```env
# Database Configuration
DB_ENGINE=postgresql  # or 'sqlite3', 'djongo'
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# MongoDB Configuration (if using)
MONGO_URI=mongodb://library_admin:your_secure_password@localhost:27017/library_db?authSource=admin

# Secret Key
SECRET_KEY=your-django-secret-key

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

Update `settings.py` to load from environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': f"django.db.backends.{os.getenv('DB_ENGINE', 'sqlite3')}",
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}
```

---

### Database Comparison

| Feature | SQLite | PostgreSQL | MongoDB |
|---------|--------|------------|---------|
| **Type** | File-based RDBMS | Relational DB | Document Store |
| **Setup** | Easy | Medium | Medium |
| **Performance** | Good | Excellent | Excellent for large scale |
| **Concurrency** | Limited | Excellent | Excellent |
| **Backup** | Copy file | pg_dump | mongodump |
| **Migrations** | Native | Native | Via Djongo |
| **Production Ready** | No | Yes | Yes |
| **ACID Compliance** | Partial | Full | Eventual (by default) |

---

## ⚙️ Backend Settings

### Complete Configuration Example (`Backend_code/backend/settings.py`)

```python
# Database (SQLite by default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
```

### Frontend API Configuration (`Frontend_code/frontend/src/services/api.js`)

```javascript
const BASE_URL = "http://localhost:8000/api/";
```

---

## 📁 Database Models

### User Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary Key |
| username | String | Unique username |
| email | String | Unique email (used for login) |
| password | String | Hashed password |
| role | String | 'ADMIN' or 'MEMBER' |
| phone | String | Optional phone number |
| address | Text | Optional address |
| is_active | Boolean | Account active status |

### Book Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary Key |
| title | String | Book title |
| author | String | Author name |
| isbn | String | Unique ISBN |
| category | String | Book category |
| quantity | Integer | Total copies |
| available_quantity | Integer | Available copies |
| cover_image | Image | Book cover |
| pdf_file | File | PDF file for reading |
| created_at | DateTime | Creation timestamp |

### Transaction Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary Key |
| user | ForeignKey | Borrowing user |
| book | ForeignKey | Borrowed book |
| issue_date | DateTime | When book was issued |
| due_date | DateTime | Return deadline |
| return_date | DateTime | When returned (nullable) |
| fine_amount | Decimal | Fine amount (₹5/day overdue) |
| status | String | 'ISSUED' or 'RETURNED' |

### Payment Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary Key |
| transaction | OneToOne | Related transaction |
| payment_reference | String | Unique payment ID |
| amount | Decimal | Payment amount |
| payment_date | DateTime | Payment timestamp |
| status | String | 'SUCCESS' or 'FAILED' |

---

## 🎨 Frontend Pages

| Page | Route | Role | Description |
|------|-------|------|-------------|
| Home | `/` | Public | Landing page |
| Login | `/login` | Public | User login |
| Register | `/register` | Public | User registration |
| Member Dashboard | `/dashboard` | Member | View borrowed books |
| Search Books | `/search` | Member | Search and issue books |
| Book Reader | `/read/:bookId` | Member | Read PDF |
| Payment | `/payment` | Member | Pay fines |
| Admin Dashboard | `/admin/dashboard` | Admin | System statistics |
| Manage Books | `/admin/books` | Admin | CRUD books |
| Add Librarian | `/admin/users` | Admin | Add librarians |

---

## 🧪 Testing

### Backend Tests

```bash
cd Backend_code
python manage.py test
```

### Frontend Linting

```bash
cd Frontend_code/frontend
npm run lint
```

---

## 📝 Notes

1. **Book Images & PDFs**: Uploaded files are stored in `Backend_code/media/`
2. **Fine Calculation**: ₹5 per day for overdue books
3. **Default Due Period**: 15 days from issue date
4. **Demo Books**: Run `seed_books.py` to populate sample data
5. **JWT Tokens**: Access token expires in 30 minutes, refresh token in 7 days

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Django Documentation: https://docs.djangoproject.com/
- React Documentation: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/
- Django REST Framework: https://www.django-rest-framework.org/

---

**Happy Reading! 📚**

