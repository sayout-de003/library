// import { useEffect, useState } from "react";
// import api from "../../services/api";
// import { motion } from "framer-motion";
// import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";

// export default function AdminDashboard() {
//   const [stats, setStats] = useState({ users: 0, books: 0, issued: 0, fines: 0 });
//   const [transactions, setTransactions] = useState([]);

//   useEffect(() => {
//     api.get("transactions/all/").then(res => {
//       setTransactions(res.data);
//       setStats({
//         users: localStorage.getItem("user") ? 1 : 0,
//         books: 100, // you can fetch real count with /books/
//         issued: res.data.filter(t => t.status === 'ISSUED').length,
//         fines: res.data.reduce((sum, t) => sum + t.fine_amount, 0)
//       });
//     });
//   }, []);

//   const pieData = [
//     { name: 'Issued', value: stats.issued },
//     { name: 'Returned', value: transactions.length - stats.issued },
//   ];
//   const COLORS = ["#0088FE", "#00C49F"];

//   return (
//     <motion.div className="p-4 space-y-6"
//       initial={{ opacity:0 }}
//       animate={{ opacity:1 }}
//       transition={{ duration:0.5 }}
//     >
//       <h2 className="text-2xl font-bold">Admin Dashboard</h2>
//       <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
//         <div className="bg-white p-4 rounded shadow">Total Users: {stats.users}</div>
//         <div className="bg-white p-4 rounded shadow">Total Books: {stats.books}</div>
//         <div className="bg-white p-4 rounded shadow">Active Issues: {stats.issued}</div>
//       </div>
//       <div className="bg-white p-4 rounded shadow">
//         <h3 className="font-semibold mb-2">Fines Collected</h3>
//         <p>Rs {stats.fines}</p>
//       </div>
//       <div className="bg-white p-4 rounded shadow">
//         <h3 className="font-semibold mb-2">Issued vs Returned Books</h3>
//         <ResponsiveContainer width="100%" height={200}>
//           <PieChart>
//             <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80}>
//               {pieData.map((entry, index) => (
//                 <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
//               ))}
//             </Pie>
//             <Tooltip />
//           </PieChart>
//         </ResponsiveContainer>
//       </div>
//     </motion.div>
//   );
// }
import { useEffect, useState } from "react";
import api from "../../services/api";
import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from "recharts";
import { BookOpen, DollarSign, Zap, BarChart3 } from "lucide-react";
import { Link } from "react-router-dom";

export default function AdminDashboard() {
  const [stats, setStats] = useState({ books: 0, issued: 0, fines: 0, totalTransactions: 0 });
  const [loading, setLoading] = useState(true);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [bookRes, transRes] = await Promise.all([
          api.get("books/"),
          api.get("transactions/all/")
        ]);

        const transactionData = transRes.data;
        const issuedCount = transactionData.filter(t => t.status === 'ISSUED').length;
        const finesTotal = transactionData.reduce((sum, t) => sum + (t.fine_amount || 0), 0);

        setStats({
          books: Array.isArray(bookRes.data) ? bookRes.data.length : bookRes.data.count || 0,
          issued: issuedCount,
          fines: finesTotal,
          totalTransactions: transactionData.length
        });
        setTransactions(transactionData.slice(0, 10)); // Latest 10 transactions
      } catch (err) {
        console.error("Failed to fetch stats:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const pieData = [
    { name: 'Issued', value: stats.issued },
    { name: 'Returned', value: stats.totalTransactions - stats.issued },
  ];
  const COLORS = ["#0088FE", "#00C49F"];

  const statusData = [
    { status: 'ISSUED', count: stats.issued },
    { status: 'RETURNED', count: stats.totalTransactions - stats.issued },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
          <p className="text-gray-400 mt-4">Loading admin dashboard...</p>
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
          <h1 className="text-4xl md:text-5xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">Manage library operations and view statistics</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Total Books */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-blue-100">Total Books</h3>
              <BookOpen size={24} className="text-blue-200" />
            </div>
            <p className="text-4xl font-bold mb-2">{stats.books}</p>
            <p className="text-xs text-blue-100">In library</p>
          </motion.div>

          {/* Active Issues */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-purple-100">Active Issues</h3>
              <Zap size={24} className="text-purple-200" />
            </div>
            <p className="text-4xl font-bold mb-2">{stats.issued}</p>
            <p className="text-xs text-purple-100">Currently issued</p>
          </motion.div>

          {/* Fines Collected */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-green-600 to-green-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-green-100">Fines Collected</h3>
              <DollarSign size={24} className="text-green-200" />
            </div>
            <p className="text-3xl font-bold mb-2">Rs {stats.fines}</p>
            <p className="text-xs text-green-100">Total fines</p>
          </motion.div>

          {/* Total Transactions */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-lg p-6 shadow-lg"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-orange-100">Transactions</h3>
              <BarChart3 size={24} className="text-orange-200" />
            </div>
            <p className="text-4xl font-bold mb-2">{stats.totalTransactions}</p>
            <p className="text-xs text-orange-100">All time</p>
          </motion.div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Pie Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
          >
            <h3 className="text-xl font-bold mb-6">Book Status Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#F3F4F6' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Bar Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
          >
            <h3 className="text-xl font-bold mb-6">Issue & Return Count</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={statusData}>
                <XAxis dataKey="status" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                <YAxis tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#F3F4F6' }}
                />
                <Bar dataKey="count" fill="#EF4444" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Recent Transactions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold">Recent Transactions</h3>
            <Link to="/admin/books" className="text-red-500 hover:text-red-400 text-sm font-semibold transition-colors">
              View All →
            </Link>
          </div>

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
                    <p className="text-sm text-gray-400">Member ID: {t.user_id}</p>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      t.status === 'ISSUED'
                        ? 'bg-blue-500 bg-opacity-30 text-blue-300'
                        : 'bg-green-500 bg-opacity-30 text-green-300'
                    }`}
                  >
                    {t.status}
                  </span>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">No transactions yet</p>
          )}
        </motion.div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            to="/admin/books"
            className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-4 px-6 rounded-lg transition-all text-center"
          >
            Manage Books
          </Link>
          <Link
            to="/admin/users"
            className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-4 px-6 rounded-lg transition-all text-center"
          >
            Add Librarian
          </Link>
        </div>
      </div>
    </motion.div>
  );
}
