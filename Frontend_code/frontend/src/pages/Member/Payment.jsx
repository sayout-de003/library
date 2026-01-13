import { useState, useEffect } from "react";
import api from "../../services/api";
import { motion } from "framer-motion";
import { CreditCard, CheckCircle, AlertCircle, DollarSign } from "lucide-react";
import { Link } from "react-router-dom";

export default function Payment() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processingId, setProcessingId] = useState(null);
  const [successId, setSuccessId] = useState(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const res = await api.get("transactions/my-history/");
        const unpaid = res.data.filter((t) => t.fine_amount > 0);
        setTransactions(unpaid);
      } catch (err) {
        console.error("Failed to fetch transactions:", err);
        setError("Failed to load transactions");
      } finally {
        setLoading(false);
      }
    };
    fetchTransactions();
  }, []);

  const payFine = async (id, amount) => {
    setProcessingId(id);
    try {
      await api.post("transactions/pay-fine/", { transaction_id: id, amount });
      setSuccessId(id);
      setTimeout(() => {
        setTransactions(transactions.filter((t) => t.id !== id));
        setSuccessId(null);
      }, 2000);
    } catch (err) {
      console.error("Payment failed:", err);
      alert(err.response?.data?.detail || "Payment failed. Please try again.");
    } finally {
      setProcessingId(null);
    }
  };

  const totalFines = transactions.reduce((sum, t) => sum + t.fine_amount, 0);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading payment information...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center p-4">
        <div className="bg-red-500 bg-opacity-20 border border-red-500 rounded-lg p-6 text-red-400 text-center max-w-md">
          <AlertCircle size={48} className="mx-auto mb-4" />
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-2 flex items-center gap-3">
            <CreditCard size={40} className="text-red-500" />
            Pay Your Fines
          </h1>
          <p className="text-gray-400">Manage and pay outstanding library fines</p>
        </motion.div>

        {/* Total Summary */}
        {transactions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gradient-to-r from-red-600 to-red-700 rounded-lg p-6 mb-8 shadow-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-red-100 text-sm mb-1">Total Amount Due</p>
                <p className="text-4xl font-bold">Rs {totalFines}</p>
                <p className="text-red-100 text-sm mt-2">
                  {transactions.length} fine{transactions.length > 1 ? "s" : ""} pending
                </p>
              </div>
              <DollarSign size={64} className="text-red-200 opacity-50" />
            </div>
          </motion.div>
        )}

        {/* Transactions List */}
        {transactions.length > 0 ? (
          <div className="space-y-4">
            {transactions.map((t, index) => (
              <motion.div
                key={t.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 * (index + 1) }}
                className={`${
                  successId === t.id
                    ? "bg-green-500 bg-opacity-20 border-green-500"
                    : "bg-gray-800 bg-opacity-50 border-gray-700"
                } border rounded-lg p-6 transition-all duration-300`}
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                  {/* Book Info */}
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {t.book?.title || "Unknown Book"}
                    </h3>
                    <p className="text-gray-400 text-sm mb-3">
                      by {t.book?.author || "Unknown Author"}
                    </p>

                    <div className="flex flex-wrap gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Due Date</p>
                        <p className="text-white font-semibold">
                          {t.due_date
                            ? new Date(t.due_date).toLocaleDateString("en-US", {
                                year: "numeric",
                                month: "short",
                                day: "numeric",
                              })
                            : "N/A"}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-500">Status</p>
                        <p className="text-blue-400 font-semibold uppercase text-xs">
                          {t.status}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Fine Amount & Button */}
                  <div className="md:text-right space-y-4">
                    <div>
                      <p className="text-gray-400 text-sm mb-1">Fine Amount</p>
                      <p className="text-3xl font-bold text-red-400">
                        Rs {t.fine_amount}
                      </p>
                    </div>

                    {successId === t.id ? (
                      <motion.div
                        initial={{ scale: 0.8 }}
                        animate={{ scale: 1 }}
                        className="flex items-center gap-2 justify-end text-green-400 font-semibold"
                      >
                        <CheckCircle size={20} fill="currentColor" />
                        Paid!
                      </motion.div>
                    ) : (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => payFine(t.id, t.fine_amount)}
                        disabled={processingId === t.id}
                        className={`w-full md:w-auto px-6 py-3 rounded-lg font-semibold transition-all ${
                          processingId === t.id
                            ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                            : "bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white"
                        }`}
                      >
                        {processingId === t.id ? (
                          <span className="flex items-center gap-2">
                            <div className="w-4 h-4 border-2 border-gray-400 border-t-white rounded-full animate-spin"></div>
                            Processing...
                          </span>
                        ) : (
                          "Pay Now"
                        )}
                      </motion.button>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          /* No Fines State */
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="bg-green-500 bg-opacity-10 border border-green-500 rounded-lg p-12 text-center"
          >
            <CheckCircle size={80} className="text-green-500 mx-auto mb-6" fill="currentColor" />
            <h2 className="text-2xl font-bold text-white mb-2">No Fines Pending!</h2>
            <p className="text-gray-400 mb-6">
              Great job! You have no outstanding fines at this time.
            </p>
            <Link
              to="/search"
              className="inline-block bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white px-8 py-3 rounded-lg font-semibold transition-all"
            >
              Explore More Books
            </Link>
          </motion.div>
        )}

        {/* Payment Methods Info */}
        {transactions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-12 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
          >
            <h3 className="text-lg font-semibold mb-4">Payment Information</h3>
            <div className="space-y-2 text-gray-400 text-sm">
              <p>💳 All payments are processed securely</p>
              <p>🔒 Your payment information is encrypted</p>
              <p>✓ Confirmation will be sent to your email</p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

