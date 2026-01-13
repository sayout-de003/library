import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Landing/Home";
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

// Member pages
import MemberDashboard from "./pages/Member/MemberDashboard";
import SearchBooks from "./pages/Member/SearchBooks";
import BookReader from "./pages/Member/BookReader";
import Payment from "./pages/Member/Payment";

// Admin pages
import AdminDashboard from "./pages/Admin/AdminDashboard";
import ManageBooks from "./pages/Admin/ManageBooks";
import AddLibrarian from "./pages/Admin/AddLibrarian";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          {/* Public */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Member Routes */}
          <Route path="/dashboard" element={<ProtectedRoute role="MEMBER"><MemberDashboard /></ProtectedRoute>} />
          <Route path="/search" element={<ProtectedRoute role="MEMBER"><SearchBooks /></ProtectedRoute>} />
          <Route path="/read/:bookId" element={<ProtectedRoute role="MEMBER"><BookReader /></ProtectedRoute>} />
          <Route path="/payment" element={<ProtectedRoute role="MEMBER"><Payment /></ProtectedRoute>} />

          {/* Admin Routes */}
          <Route path="/admin/dashboard" element={<ProtectedRoute role="ADMIN"><AdminDashboard /></ProtectedRoute>} />
          <Route path="/admin/books" element={<ProtectedRoute role="ADMIN"><ManageBooks /></ProtectedRoute>} />
          <Route path="/admin/users" element={<ProtectedRoute role="ADMIN"><AddLibrarian /></ProtectedRoute>} />
        </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
}

export default App;

