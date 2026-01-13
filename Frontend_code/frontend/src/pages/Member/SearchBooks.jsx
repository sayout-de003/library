import { useEffect, useState, useContext } from "react";
import api from "../../services/api";
import { motion, AnimatePresence } from "framer-motion";
import { Search, X } from "lucide-react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";

export default function SearchBooks() {
  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useContext(AuthContext);
  const [issuingBook, setIssuingBook] = useState(null);

  const handleIssueBook = async (bookId, bookTitle) => {
    if (!user) {
      alert("Please login to issue a book");
      return;
    }
    setIssuingBook(bookId);
    try {
      await api.post("transactions/issue/", { book_id: bookId });
      alert(`✅ "${bookTitle}" issued successfully.`);
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to issue book");
    } finally {
      setIssuingBook(null);
    }
  };

  useEffect(() => {
    const fetchBooks = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(`books/?search=${search}`);
        setBooks(res.data);
      } catch (err) {
        console.error("Failed to fetch books:", err);
        setError("Failed to load books");
      } finally {
        setLoading(false);
      }
    };

    // Debounce search
    const timeoutId = setTimeout(() => fetchBooks(), 300);
    return () => clearTimeout(timeoutId);
  }, [search]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white">
      {/* Search Header */}
      <div className="sticky top-16 z-40 bg-black bg-opacity-95 backdrop-blur-md border-b border-gray-800 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">Search Library</h1>

          {/* Search Input */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={24} />
            <input
              type="text"
              placeholder="Search books by title, author, or category..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 text-white placeholder-gray-400 transition-all duration-200"
            />
            {search && (
              <button
                onClick={() => setSearch("")}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
              >
                <X size={20} />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Loading State */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center py-12"
            >
              <div className="inline-block">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
                <p className="text-gray-400 mt-4">Searching...</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error State */}
        {error && !loading && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-500 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400 text-center"
          >
            {error}
          </motion.div>
        )}

        {/* Books Grid */}
        {!loading && books.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ staggerChildren: 0.1 }}
            className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"
          >
            <AnimatePresence>
              {books.map((book) => (
                <motion.div
                  key={book.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  whileHover={{ scale: 1.08, y: -5 }}
                  whileTap={{ scale: 0.95 }}
                  className="group cursor-pointer"
                >
                  <Link to={`/read/${book.id}`}>
                    <div className="relative h-[220px] sm:h-[260px] rounded-lg overflow-hidden shadow-lg bg-gray-800">
                      <img
                        src={
                          book.cover_image
                            ? `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${book.cover_image}`
                            : "/placeholder-book.svg"
                        }
                        alt={book.title}
                        className="w-full h-full object-cover group-hover:brightness-50 transition-all duration-300"
                        onError={(e) => {
                          e.target.src = "/placeholder-book.svg";
                        }}
                      />

                      {/* Overlay */}
                      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 p-4 space-y-3">
                        <Link
                          to={`/read/${book.id}`}
                          className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-all w-full justify-center"
                        >
                          View Details
                        </Link>
                        {user && user.role === "MEMBER" && (
                          <button
                            onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              handleIssueBook(book.id, book.title);
                            }}
                            disabled={issuingBook === book.id}
                            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold transition-all w-full justify-center disabled:opacity-50"
                          >
                            {issuingBook === book.id ? "Issuing..." : "Issue"}
                          </button>
                        )}
                      </div>
                    </div>

                    {/* Book Info */}
                    <div className="mt-3 px-1">
                      <h3 className="font-semibold text-sm line-clamp-2 group-hover:text-red-500 transition-colors">
                        {book.title}
                      </h3>
                      <p className="text-xs text-gray-400 mt-1 truncate">{book.author}</p>
                      {book.category && <p className="text-xs text-gray-500 mt-1">{book.category}</p>}
                    </div>
                  </Link>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        )}

        {/* Empty State */}
        {!loading && !error && books.length === 0 && search && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-20"
          >
            <p className="text-gray-400 text-lg mb-4">No books found matching "{search}"</p>
            <button
              onClick={() => setSearch("")}
              className="text-red-500 hover:text-red-400 font-semibold transition-colors"
            >
              Clear search
            </button>
          </motion.div>
        )}

        {/* Initial State */}
        {!loading && !error && books.length === 0 && !search && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-20"
          >
            <Search size={64} className="text-gray-600 mx-auto mb-4 opacity-50" />
            <p className="text-gray-400 text-lg">Start searching to discover amazing books</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
