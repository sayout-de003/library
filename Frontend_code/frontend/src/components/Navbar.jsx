import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { Menu, X, LogOut, Home, Search, BarChart3, Settings, RotateCcw } from "lucide-react";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isAdmin = user && (user.role === "ADMIN" || user.is_superuser || user.is_staff);

  const handleLogout = () => {
    logout();
    setMobileMenuOpen(false);
  };

  return (
    <motion.nav
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 bg-gradient-to-r from-black via-gray-900 to-black border-b border-gray-800 shadow-lg"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex-shrink-0 flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-r from-red-600 to-red-700 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">📚</span>
            </div>
            <span className="text-xl font-bold text-white hidden sm:inline">BookHub</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-2">
            {user ? (
              <>
                {/* Common Links */}
                <Link
                  to="/"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                >
                  <Home size={18} /> Home
                </Link>

                {/* Role-based Links */}
                {!isAdmin ? (
                  <>
                    <Link
                      to="/search"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                    >
                      <Search size={18} /> Browse
                    </Link>
                    <Link
                      to="/dashboard"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                    >
                      <RotateCcw size={18} /> Return
                    </Link>
                    <Link
                      to="/dashboard"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                    >
                      <BarChart3 size={18} /> Dashboard
                    </Link>
                    <Link
                      to="/payment"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all"
                    >
                      Payments
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to="/admin/dashboard"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                    >
                      <BarChart3 size={18} /> Dashboard
                    </Link>
                    <Link
                      to="/admin/books"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all flex items-center gap-2"
                    >
                      <Settings size={18} /> Manage
                    </Link>
                    <Link
                      to="/admin/users"
                      className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all"
                    >
                      Users
                    </Link>
                  </>
                )}

                {/* User Profile */}
                <div className="flex items-center gap-4 ml-4 pl-4 border-l border-gray-700">
                  <div className="text-right">
                    <p className="text-sm font-semibold text-white">{user.username}</p>
                    <p className="text-xs text-gray-400 uppercase tracking-wider">{user.role}</p>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleLogout}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-all flex items-center gap-2 font-semibold"
                  >
                    <LogOut size={16} /> Logout
                  </motion.button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all"
                >
                  Home
                </Link>
                <Link
                  to="/login"
                  className="text-gray-300 hover:text-white px-3 py-2 rounded-lg hover:bg-gray-800 transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-all font-semibold"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-gray-300 hover:text-white p-2"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="md:hidden bg-gray-800 border-t border-gray-700 py-4 space-y-2"
          >
            {user ? (
              <>
                <Link
                  to="/"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                >
                  Home
                </Link>
                {!isAdmin ? (
                  <>
                    <Link
                      to="/search"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Browse Books
                    </Link>
                    <Link
                      to="/dashboard"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Return Book
                    </Link>
                    <Link
                      to="/payment"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Payments
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to="/admin/dashboard"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Admin Dashboard
                    </Link>
                    <Link
                      to="/admin/books"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Manage Books
                    </Link>
                    <Link
                      to="/admin/users"
                      onClick={() => setMobileMenuOpen(false)}
                      className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                    >
                      Manage Users
                    </Link>
                  </>
                )}
                <button
                  onClick={handleLogout}
                  className="w-full text-left text-red-400 hover:text-red-300 px-4 py-2 rounded hover:bg-gray-700 transition-all"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                >
                  Home
                </Link>
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block text-gray-300 hover:text-white px-4 py-2 rounded hover:bg-gray-700 transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-all text-center font-semibold"
                >
                  Register
                </Link>
              </>
            )}
          </motion.div>
        )}
      </div>
    </motion.nav>
  );
}
