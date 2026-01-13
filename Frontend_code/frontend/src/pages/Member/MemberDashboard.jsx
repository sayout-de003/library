import { useEffect, useState } from "react";
import api from "../../services/api";
import { motion } from "framer-motion";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { BookOpen, AlertCircle, RotateCcw, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

export default function MemberDashboard() {
  const [transactions, setTransactions] = useState([]);
  const [totalFines, setTotalFines] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [returningTx, setReturningTx] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("transactions/my-history/");
        setTransactions(res.data);
        const fines = res.data.reduce((sum, t) => sum + (t.fine_amount || 0), 0);
        setTotalFines(fines);
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const chartData = transactions
    .filter(t => t.fine_amount > 0)
    .slice(0, 10)
    .map(t => ({
      name: (t.book?.title || 'Unknown Book').slice(0, 15),
      fine: t.fine_amount,
    }));

  const issuedCount = transactions.filter(t => t.status === 'ISSUED').length;
  const returnedCount = transactions.filter(t => t.status === 'RETURNED').length;

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center p-4">
        <div className="bg-red-500 bg-opacity-20 border border-red-500 rounded-lg p-6 text-red-400 text-center">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white"
    >
      <div className="max-w-7xl mx-auto px-6 py-12 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl md:text-5xl font-bold mb-2">My Library Dashboard</h1>
          <p className="text-gray-400">Manage your books, fines, and transactions</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Total Fines */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-red-600 to-red-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-red-100">Total Fines Due</h3>
              <AlertCircle size={24} className="text-red-200" />
            </div>
            <p className="text-3xl font-bold mb-2">Rs {totalFines}</p>
            {totalFines > 0 && (
              <Link
                to="/payment"
                className="text-sm text-red-100 hover:text-white transition-colors underline"
              >
                Pay now →
              </Link>
            )}
          </motion.div>

          {/* Books Issued */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-blue-100">Books Issued</h3>
              <BookOpen size={24} className="text-blue-200" />
            </div>
            <p className="text-3xl font-bold">{issuedCount}</p>
            <p className="text-xs text-blue-100 mt-2">Currently active</p>
          </motion.div>

          {/* Books Returned */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-green-600 to-green-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-green-100">Books Returned</h3>
              <RotateCcw size={24} className="text-green-200" />
            </div>
            <p className="text-3xl font-bold">{returnedCount}</p>
            <p className="text-xs text-green-100 mt-2">Total returned</p>
          </motion.div>

          {/* Total Transactions */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-purple-100">Total Transactions</h3>
              <TrendingUp size={24} className="text-purple-200" />
            </div>
            <p className="text-3xl font-bold">{transactions.length}</p>
            <p className="text-xs text-purple-100 mt-2">All time</p>
          </motion.div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Transactions List */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
            >
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <BookOpen size={24} className="text-red-500" />
                Your Library Activity
              </h2>

              {transactions.length > 0 ? (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {transactions.map((t) => (
                    <motion.div
                      key={t.id}
                      whileHover={{ x: 5 }}
                      className="flex justify-between items-center bg-gray-700 bg-opacity-50 p-4 rounded-lg border border-gray-600 hover:border-gray-500 transition-all"
                    >
                      <div className="flex-1">
                        <p className="font-semibold text-white">{t.book?.title || 'Unknown Book'}</p>
                        <p className="text-sm text-gray-400">by {t.book?.author || 'Unknown'}</p>
                      </div>

                      <div className="flex items-center gap-6">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            t.status === 'ISSUED'
                              ? 'bg-blue-500 bg-opacity-30 text-blue-300'
                              : 'bg-green-500 bg-opacity-30 text-green-300'
                          }`}
                        >
                          {t.status}
                        </span>

                        {t.fine_amount > 0 && (
                          <span className="font-semibold text-red-400">
                            Fine: Rs {t.fine_amount}
                          </span>
                        )}

                        {t.status === 'ISSUED' && (
                          <button
                            onClick={async () => {
                              if (!confirm('Return this book now?')) return;
                              setReturningTx(t.id);
                              try {
                                const res = await api.post('transactions/return/', { transaction_id: t.id });
                                // update transaction in local state
                                setTransactions((prev) => prev.map(item => item.id === t.id ? res.data : item));
                                alert('Book returned successfully');
                              } catch (err) {
                                console.error('Return failed', err);
                                alert(err.response?.data?.detail || 'Failed to return book');
                              } finally {
                                setReturningTx(null);
                              }
                            }}
                            disabled={returningTx === t.id}
                            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-md text-sm font-semibold"
                          >
                            {returningTx === t.id ? 'Returning...' : 'Return'}
                          </button>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <BookOpen size={48} className="text-gray-600 mx-auto mb-4 opacity-50" />
                  <p className="text-gray-400">No transactions yet. Start exploring books!</p>
                </div>
              )}
            </motion.div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
            >
              <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Link
                  to="/search"
                  className="block w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 px-4 rounded-lg transition-all text-center"
                >
                  Explore Books
                </Link>
                {totalFines > 0 && (
                  <Link
                    to="/payment"
                    className="block w-full bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800 text-white font-semibold py-3 px-4 rounded-lg transition-all text-center"
                  >
                    Pay Fines
                  </Link>
                )}
              </div>
            </motion.div>

            {/* Status Info */}
            {totalFines === 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-green-500 bg-opacity-20 border border-green-500 rounded-lg p-6"
              >
                <p className="text-green-400 font-semibold text-center">✓ No fines pending!</p>
                <p className="text-green-300 text-sm text-center mt-2">Keep it up!</p>
              </motion.div>
            )}
          </div>
        </div>

        {/* Fines Chart */}
        {chartData.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
          >
            <h3 className="text-xl font-bold mb-6">Fines Overview (Top Books)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#9CA3AF' }} />
                <YAxis tick={{ fontSize: 12, fill: '#9CA3AF' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#F3F4F6' }}
                />
                <Bar dataKey="fine" fill="#EF4444" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

