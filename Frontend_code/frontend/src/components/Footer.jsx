import { Link } from "react-router-dom";
import { Facebook, Twitter, Instagram, Mail } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-black border-t border-gray-800 text-gray-400 mt-16">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
              <span className="text-red-500">📚</span> BookHub
            </h3>
            <p className="text-sm">
              Your digital library for discovering, reading, and managing books online.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/search" className="hover:text-white transition-colors">
                  Browse Books
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-white transition-colors">
                  Sign In
                </Link>
              </li>
            </ul>
          </div>

          {/* Help */}
          <div>
            <h4 className="text-white font-semibold mb-4">Help & Support</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  FAQs
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white transition-colors">
                  Report Issue
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-semibold mb-4">Connect With Us</h4>
            <div className="flex gap-4">
              <a href="#" className="hover:text-red-500 transition-colors">
                <Facebook size={20} />
              </a>
              <a href="#" className="hover:text-red-500 transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" className="hover:text-red-500 transition-colors">
                <Instagram size={20} />
              </a>
              <a href="#" className="hover:text-red-500 transition-colors">
                <Mail size={20} />
              </a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800 my-8"></div>

        {/* Bottom Footer */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm">
          <p>
            &copy; {currentYear} <span className="text-white font-semibold">BookHub</span>. All rights reserved.
          </p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Terms of Service
            </a>
            <a href="#" className="hover:text-white transition-colors">
              Cookie Settings
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

