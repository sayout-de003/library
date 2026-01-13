import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Document, Page, pdfjs } from "react-pdf";
import api from "../../services/api";
import { motion } from "framer-motion";
import { ArrowLeft, AlertTriangle } from "lucide-react";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function BookReader() {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const res = await api.get(`books/${bookId}/`);
        setBook(res.data);
      } catch (err) {
        console.error("Failed to fetch book:", err);
        setError("Failed to load book");
      } finally {
        setLoading(false);
      }
    };
    fetchBook();
  }, [bookId]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading book...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center p-4">
        <div className="bg-red-500 bg-opacity-20 border border-red-500 rounded-lg p-6 text-red-400 text-center max-w-md">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!book) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <p className="text-gray-400">Book not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white">
      {/* Header */}
      <div className="sticky top-16 z-40 bg-black bg-opacity-95 backdrop-blur-md border-b border-gray-800 p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
          >
            <ArrowLeft size={24} />
            <span className="hidden sm:inline">Back</span>
          </button>
          <h1 className="text-xl font-bold truncate flex-1 px-4">{book.title}</h1>
          <p className="text-gray-400 text-sm hidden sm:block">
            {currentPage} of {numPages || "..."}
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Book Info */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
        >
          <div className="flex flex-col sm:flex-row gap-6">
            <img
              src={
                book.cover_image
                  ? `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${book.cover_image}`
                  : "/placeholder-book.svg"
              }
              alt={book.title}
              className="w-32 h-48 object-cover rounded-lg shadow-lg"
              onError={(e) => {
                e.target.src = "/placeholder-book.svg";
              }}
            />
            <div className="flex-1">
              <h2 className="text-3xl font-bold mb-2">{book.title}</h2>
              <p className="text-gray-300 text-lg mb-4">by {book.author}</p>
              {book.category && (
                <div className="inline-block bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold mb-4">
                  {book.category}
                </div>
              )}
              <p className="text-gray-400 mt-4">
                Ready to read? Scroll down to start browsing the book.
              </p>
            </div>
          </div>
        </motion.div>

        {/* PDF Reader */}
        {book.pdf_file ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-900 rounded-lg overflow-hidden shadow-2xl"
          >
            <div className="bg-gray-800 p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="text-sm text-gray-400">
                Page <span className="text-white font-semibold">{currentPage}</span> of{" "}
                <span className="text-white font-semibold">{numPages || "..."}</span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-600 rounded-lg font-semibold transition-all"
                >
                  ← Previous
                </button>
                <button
                  onClick={() => setCurrentPage(Math.min(numPages, currentPage + 1))}
                  disabled={currentPage === numPages}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-600 rounded-lg font-semibold transition-all"
                >
                  Next →
                </button>
              </div>
            </div>

            <div className="overflow-auto max-h-[70vh] flex justify-center bg-black p-4">
              <Document
                file={`${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}${book.pdf_file}`}
                onLoadSuccess={onDocumentLoadSuccess}
                onLoadError={(error) => {
                  console.error("Error loading PDF:", error);
                  setError("Failed to load PDF file");
                }}
                loading={
                  <div className="flex justify-center items-center h-64">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600 mx-auto"></div>
                      <p className="text-gray-400 mt-4">Loading PDF...</p>
                    </div>
                  </div>
                }
              >
                <Page pageNumber={currentPage} />
              </Document>
            </div>

            <div className="bg-gray-800 p-4 text-center text-sm text-gray-400">
              {numPages && numPages > 1 && (
                <p>
                  Page {currentPage} of {numPages} • Keep reading!
                </p>
              )}
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-yellow-500 bg-opacity-20 border border-yellow-500 rounded-lg p-12 text-center"
          >
            <AlertTriangle size={64} className="text-yellow-500 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">PDF Not Available</h3>
            <p className="text-gray-300 mb-4">
              This book doesn't have a PDF file attached yet. Please contact the library administrator.
            </p>
            <button
              onClick={() => navigate(-1)}
              className="inline-block bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-all"
            >
              Go Back
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}

