import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../services/api";
import { motion } from "framer-motion";
import { Mail, Lock, User, Eye, EyeOff, CheckCircle } from "lucide-react";

export default function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const validateForm = () => {
    if (!email || !username || !password || !confirmPassword) {
      setError("All fields are required");
      return false;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return false;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return false;
    }
    if (username.length < 3) {
      setError("Username must be at least 3 characters");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!validateForm()) return;

    setLoading(true);
    try {
      await api.post("auth/register/", { email, username, password });
      setSuccess(true);
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.email?.[0] ||
          err.response?.data?.username?.[0] ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 0.6 }}
            className="mb-6"
          >
            <CheckCircle size={80} className="text-green-500 mx-auto" fill="currentColor" />
          </motion.div>
          <h2 className="text-3xl font-bold text-white mb-2">Welcome to BookHub!</h2>
          <p className="text-gray-400 mb-4">Your account has been created successfully.</p>
          <p className="text-gray-500">Redirecting to login...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center p-4">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-0 w-96 h-96 bg-red-600 opacity-10 rounded-full filter blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-red-600 opacity-10 rounded-full filter blur-3xl"></div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-white mb-2">BookHub</h1>
          <p className="text-gray-400">Join Our Reading Community</p>
        </div>

        {/* Form Card */}
        <div className="bg-gray-900 bg-opacity-80 backdrop-blur-md border border-gray-800 rounded-2xl p-8 shadow-2xl">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">Create Account</h2>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-500 bg-opacity-20 border border-red-500 rounded-lg text-red-400 text-sm"
            >
              {error}
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-3.5 text-gray-500" size={20} />
                <input
                  type="text"
                  placeholder="Choose a username"
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500 text-white placeholder-gray-500 transition-all duration-200"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3.5 text-gray-500" size={20} />
                <input
                  type="email"
                  placeholder="you@example.com"
                  className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500 text-white placeholder-gray-500 transition-all duration-200"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3.5 text-gray-500" size={20} />
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="At least 6 characters"
                  className="w-full pl-10 pr-10 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500 text-white placeholder-gray-500 transition-all duration-200"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3.5 text-gray-500 hover:text-gray-300 transition-colors"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Confirm Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Confirm Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3.5 text-gray-500" size={20} />
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Confirm password"
                  className="w-full pl-10 pr-10 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-red-500 focus:outline-none focus:ring-1 focus:ring-red-500 text-white placeholder-gray-500 transition-all duration-200"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-3.5 text-gray-500 hover:text-gray-300 transition-colors"
                >
                  {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Register Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white font-bold rounded-lg hover:from-red-700 hover:to-red-800 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-1 h-px bg-gray-700"></div>
            <span className="px-4 text-gray-500 text-sm">or</span>
            <div className="flex-1 h-px bg-gray-700"></div>
          </div>

          {/* Login Link */}
          <p className="text-center text-gray-400">
            Already have an account?{" "}
            <Link to="/login" className="text-red-500 font-semibold hover:text-red-400 transition-colors">
              Sign in
            </Link>
          </p>
        </div>

        {/* Footer Text */}
        <p className="text-center text-gray-500 text-sm mt-6">
          By registering, you agree to our Terms of Service
        </p>
      </motion.div>
    </div>
  );
}
