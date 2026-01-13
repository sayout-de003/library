import os
import sys
import django
import random

# 1. SETUP DJANGO ENVIRONMENT
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Set the correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

from books.models import Book

print("Environment set up successfully.")
print("Preparing to seed 100 new books...")

# 2. DEFINE 100 BOOKS (Title, Author, Category)
# We will generate ISBNs automatically in the loop below.
books_source = [
    # --- TECHNOLOGY (20) ---
    ("Refactoring", "Martin Fowler", "Technology"),
    ("Domain-Driven Design", "Eric Evans", "Technology"),
    ("The Phoenix Project", "Gene Kim", "Technology"),
    ("Building Microservices", "Sam Newman", "Technology"),
    ("Test Driven Development", "Kent Beck", "Technology"),
    ("Working Effectively with Legacy Code", "Michael Feathers", "Technology"),
    ("Head First Design Patterns", "Eric Freeman", "Technology"),
    ("You Don't Know JS", "Kyle Simpson", "Technology"),
    ("Grokking Algorithms", "Aditya Bhargava", "Technology"),
    ("Code Complete", "Steve McConnell", "Technology"),
    ("The Mythical Man-Month", "Fred Brooks", "Technology"),
    ("Soft Skills", "John Sonmez", "Technology"),
    ("Don't Make Me Think", "Steve Krug", "Technology"),
    ("Hooked", "Nir Eyal", "Technology"),
    ("The Lean Startup", "Eric Ries", "Technology"),
    ("Sprint", "Jake Knapp", "Technology"),
    ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Technology"),
    ("Python Crash Course", "Eric Matthes", "Technology"),
    ("Effective Java", "Joshua Bloch", "Technology"),
    ("Deep Learning", "Ian Goodfellow", "Technology"),

    # --- SCIENCE FICTION (15) ---
    ("Foundation", "Isaac Asimov", "Science Fiction"),
    ("Foundation and Empire", "Isaac Asimov", "Science Fiction"),
    ("Second Foundation", "Isaac Asimov", "Science Fiction"),
    ("Neuromancer", "William Gibson", "Science Fiction"),
    ("Snow Crash", "Neal Stephenson", "Science Fiction"),
    ("The Three-Body Problem", "Cixin Liu", "Science Fiction"),
    ("The Dark Forest", "Cixin Liu", "Science Fiction"),
    ("Death's End", "Cixin Liu", "Science Fiction"),
    ("Hyperion", "Dan Simmons", "Science Fiction"),
    ("Ender's Game", "Orson Scott Card", "Science Fiction"),
    ("Ready Player One", "Ernest Cline", "Science Fiction"),
    ("Brave New World", "Aldous Huxley", "Science Fiction"),
    ("Fahrenheit 451", "Ray Bradbury", "Science Fiction"),
    ("Jurassic Park", "Michael Crichton", "Science Fiction"),
    ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction"),

    # --- FANTASY (15) ---
    ("The Fellowship of the Ring", "J.R.R. Tolkien", "Fantasy"),
    ("The Two Towers", "J.R.R. Tolkien", "Fantasy"),
    ("The Return of the King", "J.R.R. Tolkien", "Fantasy"),
    ("The Way of Kings", "Brandon Sanderson", "Fantasy"),
    ("Words of Radiance", "Brandon Sanderson", "Fantasy"),
    ("Oathbringer", "Brandon Sanderson", "Fantasy"),
    ("Mistborn: The Final Empire", "Brandon Sanderson", "Fantasy"),
    ("American Gods", "Neil Gaiman", "Fantasy"),
    ("Good Omens", "Neil Gaiman & Terry Pratchett", "Fantasy"),
    ("The Colour of Magic", "Terry Pratchett", "Fantasy"),
    ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", "Fantasy"),
    ("Harry Potter and the Goblet of Fire", "J.K. Rowling", "Fantasy"),
    ("The Golden Compass", "Philip Pullman", "Fantasy"),
    ("Eragon", "Christopher Paolini", "Fantasy"),
    ("Percy Jackson & The Lightning Thief", "Rick Riordan", "Fantasy"),

    # --- CLASSICS (15) ---
    ("War and Peace", "Leo Tolstoy", "Classic"),
    ("Anna Karenina", "Leo Tolstoy", "Classic"),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Classic"),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", "Classic"),
    ("Moby Dick", "Herman Melville", "Classic"),
    ("Great Expectations", "Charles Dickens", "Classic"),
    ("A Tale of Two Cities", "Charles Dickens", "Classic"),
    ("Jane Eyre", "Charlotte Bronte", "Classic"),
    ("Wuthering Heights", "Emily Bronte", "Classic"),
    ("Frankenstein", "Mary Shelley", "Classic"),
    ("Dracula", "Bram Stoker", "Classic"),
    ("The Odyssey", "Homer", "Classic"),
    ("The Iliad", "Homer", "Classic"),
    ("Don Quixote", "Miguel de Cervantes", "Classic"),
    ("Les Misérables", "Victor Hugo", "Classic"),

    # --- MYSTERY & THRILLER (15) ---
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery"),
    ("The Girl Who Played with Fire", "Stieg Larsson", "Mystery"),
    ("The Girl Who Kicked the Hornet's Nest", "Stieg Larsson", "Mystery"),
    ("And Then There Were None", "Agatha Christie", "Mystery"),
    ("Murder on the Orient Express", "Agatha Christie", "Mystery"),
    ("The Big Sleep", "Raymond Chandler", "Mystery"),
    ("In Cold Blood", "Truman Capote", "Thriller"),
    ("Sharp Objects", "Gillian Flynn", "Thriller"),
    ("Dark Places", "Gillian Flynn", "Thriller"),
    ("Big Little Lies", "Liane Moriarty", "Thriller"),
    ("The Woman in the Window", "A.J. Finn", "Thriller"),
    ("Behind Closed Doors", "B.A. Paris", "Thriller"),
    ("The Hound of the Baskervilles", "Arthur Conan Doyle", "Mystery"),
    ("A Study in Scarlet", "Arthur Conan Doyle", "Mystery"),
    ("Angels & Demons", "Dan Brown", "Thriller"),

    # --- HISTORY & BIOGRAPHY (10) ---
    ("The Silk Roads", "Peter Frankopan", "History"),
    ("Guns, Germs, and Steel", "Jared Diamond", "History"),
    ("1776", "David McCullough", "History"),
    ("Alexander Hamilton", "Ron Chernow", "Biography"),
    ("Elon Musk", "Ashlee Vance", "Biography"),
    ("Shoe Dog", "Phil Knight", "Biography"),
    ("Becoming", "Michelle Obama", "Biography"),
    ("Born a Crime", "Trevor Noah", "Biography"),
    ("Into the Wild", "Jon Krakauer", "Biography"),
    ("Unbroken", "Laura Hillenbrand", "History"),

    # --- FINANCE (10) ---
    ("The Intelligent Investor", "Benjamin Graham", "Finance"),
    ("One Up On Wall Street", "Peter Lynch", "Finance"),
    ("Common Stocks and Uncommon Profits", "Philip Fisher", "Finance"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "Finance"),
    ("Think and Grow Rich", "Napoleon Hill", "Finance"),
    ("The Millionaire Next Door", "Thomas J. Stanley", "Finance"),
    ("Your Money or Your Life", "Vicki Robin", "Finance"),
    ("I Will Teach You to Be Rich", "Ramit Sethi", "Finance"),
    ("Principles", "Ray Dalio", "Finance"),
    ("Freakonomics", "Stephen J. Dubner", "Finance"),
]

# 3. CREATE OBJECTS WITH GENERATED ISBNs
objs = []
start_isbn = 9789990000001  # Starting with a high 'fake' range to avoid conflicts

for i, (title, author, category) in enumerate(books_source):
    # Generate unique ISBN based on the counter
    generated_isbn = str(start_isbn + i)
    
    # Check if this specific ISBN already exists (unlikely given the high range)
    if not Book.objects.filter(isbn=generated_isbn).exists():
        objs.append(
            Book(
                title=title,
                author=author,
                isbn=generated_isbn,
                category=category,
                quantity=random.randint(5, 30), # Randomize stock between 5 and 30
                available_quantity=random.randint(1, 5), # Randomize availability
                cover_image="" 
            )
        )

# 4. BULK INSERT
if objs:
    Book.objects.bulk_create(objs)
    print(f"\nSuccessfully added {len(objs)} books!")
else:
    print("\nNo books added (ISBNs might already exist).")