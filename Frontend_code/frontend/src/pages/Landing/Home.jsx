import { useEffect, useState } from "react";
import api from "../../services/api";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight, Play, Info, BookOpen, RotateCcw, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

export default function Home() {
  const { user } = useContext(AuthContext);
  const [booksByCategory, setBooksByCategory] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [featuredBook, setFeaturedBook] = useState(null);
  const [issuingBook, setIssuingBook] = useState(null);
  const [returningBook, setReturningBook] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    api.get("books/by-category/")
      .then(res => {
        setBooksByCategory(res.data);
        const categories = Object.keys(res.data);
        if (categories.length > 0 && res.data[categories[0]].length > 0) {
          setFeaturedBook(res.data[categories[0]][0]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch books:", err);
        setError("Failed to load books");
        setLoading(false);
      });
  }, []);

  const handleIssueBook = async (bookId, bookTitle) => {
    if (!user) {
      alert("Please login to issue a book");
      return;
    }

    setIssuingBook(bookId);
    try {
      await api.post("transactions/issue/", { book_id: bookId });
      setSuccessMessage(`✅ "${bookTitle}" has been issued successfully!`);
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to issue book");
    } finally {
      setIssuingBook(null);
    }
  };

  const handleReturnBook = async (bookId, bookTitle) => {
    if (!user) {
      alert("Please login to return a book");
      return;
    }

    // Returning by book is not supported by backend (requires transaction_id)
    alert("Please return books from your Dashboard -> Your Library Activity.");
  };

  const scrollCategory = (categoryKey, direction) => {
    const container = document.getElementById(`category-${categoryKey}`);
    if (container) {
      const scrollAmount = 400;
      container.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <div className="text-center">
          <div className="animate-pulse">
            <p className="text-gray-400 text-lg">Loading Library...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    );
  }

  const categories = Object.keys(booksByCategory);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white">
      {/* Featured Hero Section */}
      {featuredBook && (
        <div className="relative h-[500px] md:h-[600px] overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent z-10"></div>
          <img
            src={
              featuredBook.cover_image
                ? `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${featuredBook.cover_image}`
                : "/placeholder-book.svg"
            }
            alt={featuredBook.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            onError={(e) => {
              e.target.src = "/placeholder-book.svg";
            }}
          />

          {/* Hero Content */}
          <div className="absolute inset-0 flex items-end z-20 p-6 md:p-12">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="w-full md:w-1/2"
            >
              <h1 className="text-4xl md:text-5xl font-black mb-4 drop-shadow-lg">
                {featuredBook.title}
              </h1>
              <p className="text-gray-200 text-sm md:text-base mb-6 drop-shadow-lg">
                By <span className="font-semibold">{featuredBook.author}</span>
              </p>
              {featuredBook.category && (
                <div className="inline-block bg-red-600 text-white px-4 py-1 rounded-full text-sm font-semibold mb-6">
                  {featuredBook.category}
                </div>
              )}
              <div className="flex gap-4">
                <Link
                  to="/search"
                  className="flex items-center gap-2 bg-white text-black px-8 py-3 rounded-lg font-bold hover:bg-gray-200 transition-all duration-200 transform hover:scale-105"
                >
                  <Play size={20} fill="currentColor" /> Explore
                </Link>
                <button className="flex items-center gap-2 bg-gray-600 bg-opacity-70 text-white px-8 py-3 rounded-lg font-semibold hover:bg-opacity-50 transition-all">
                  <Info size={20} /> More Info
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}

      {/* Success Message */}
      {successMessage && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="fixed top-20 left-1/2 transform -translate-x-1/2 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50"
        >
          {successMessage}
        </motion.div>
      )}

      {/* Categories Section */}
      <div className="px-6 md:px-12 py-12 space-y-12">
        {categories.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-400 text-lg">No books available yet</p>
          </div>
        ) : (
          categories.map((category) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
            >
              {/* Category Title */}
              <div className="mb-6">
                <h2 className="text-2xl md:text-3xl font-bold mb-2">{category}</h2>
                <div className="h-1 w-20 bg-red-600 rounded-full"></div>
              </div>

              {/* Books Carousel */}
              <div className="relative group">
                {/* Left Arrow */}
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => scrollCategory(category, "left")}
                  className="absolute left-0 top-1/2 -translate-y-1/2 z-20 bg-black bg-opacity-50 hover:bg-opacity-70 p-2 rounded-full transition-all duration-200 opacity-0 group-hover:opacity-100"
                >
                  <ChevronLeft size={28} className="text-white" />
                </motion.button>

                {/* Books Container */}
                <div
                  id={`category-${category}`}
                  className="flex gap-4 overflow-x-auto scroll-smooth scrollbar-hide pb-4"
                >
                  {booksByCategory[category].map((book) => (
                    <motion.div
                      key={book.id}
                      whileHover={{ scale: 1.08, y: -10 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex-shrink-0 w-[160px] md:w-[200px] cursor-pointer group/book"
                    >
                      <div className="relative h-[240px] md:h-[300px] rounded-lg overflow-hidden shadow-lg">
                        <img
                          src={
                            book.cover_image
                              ? `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${book.cover_image}`
                              : "/placeholder-book.svg"
                          }
                          alt={book.title}
                          className="w-full h-full object-cover group-hover/book:brightness-50 transition-all duration-300"
                          onError={(e) => {
                            e.target.src = "/placeholder-book.svg";
                          }}
                        />
                        {/* Overlay on Hover */}
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover/book:bg-opacity-70 transition-all duration-300 flex flex-col items-center justify-center opacity-0 group-hover/book:opacity-100 p-4 space-y-3">
                          <Link
                            to="/search"
                            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-all w-full justify-center"
                          >
                            <Play size={18} fill="white" /> Read
                          </Link>
                          {user && user.role === "MEMBER" && (
                            <>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleIssueBook(book.id, book.title);
                                }}
                                disabled={issuingBook === book.id}
                                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition-all w-full justify-center disabled:opacity-50"
                              >
                                <BookOpen size={18} /> {issuingBook === book.id ? "Issuing..." : "Issue"}
                              </button>
                            </>
                          )}
                        </div>
                      </div>
                      {/* Book Info */}
                      <div className="mt-3">
                        <p className="font-semibold text-sm line-clamp-2 hover:text-red-500 transition-colors">
                          {book.title}
                        </p>
                        <p className="text-xs text-gray-400 mt-1">{book.author}</p>
                      </div>
                    </motion.div>
                  ))}
                </div>

                {/* Right Arrow */}
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => scrollCategory(category, "right")}
                  className="absolute right-0 top-1/2 -translate-y-1/2 z-20 bg-black bg-opacity-50 hover:bg-opacity-70 p-2 rounded-full transition-all duration-200 opacity-0 group-hover:opacity-100"
                >
                  <ChevronRight size={28} className="text-white" />
                </motion.button>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}

