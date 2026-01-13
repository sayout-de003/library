import { useEffect, useState } from "react";
import api from "../../services/api";
import { motion } from "framer-motion";
import Button from "../../components/Button";

export default function ManageBooks() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [category, setCategory] = useState("");
  const [coverImage, setCoverImage] = useState(null);
  const [editing, setEditing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBooks = async () => {
    try {
      const res = await api.get("books/");
      setBooks(res.data);
    } catch (err) {
      console.error("Failed to fetch books:", err);
      setError("Failed to load books");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleAddOrEdit = async e => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append("title", title);
    formData.append("author", author);
    formData.append("category", category);
    
    if (coverImage) {
      formData.append("cover_image", coverImage);
    }

    try {
      if (editing) {
        // For editing, we'll use PUT and only include cover_image if changed
        const data = { title, author, category };
        await api.put(`books/${editing.id}/`, data);
        setEditing(null);
      } else {
        await api.post("books/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      }
      
      // Reset form
      setTitle("");
      setAuthor("");
      setCategory("");
      setCoverImage(null);
      
      // Refresh book list
      fetchBooks();
    } catch (err) {
      console.error("Failed to save book:", err);
      alert(err.response?.data?.detail || "Failed to save book");
    }
  };

  const handleDelete = async id => {
    if (confirm("Are you sure you want to delete this book?")) {
      try {
        await api.delete(`books/${id}/`);
        fetchBooks();
      } catch (err) {
        console.error("Failed to delete book:", err);
        alert(err.response?.data?.detail || "Failed to delete book");
      }
    }
  };

  const handleEdit = book => {
    setEditing(book);
    setTitle(book.title);
    setAuthor(book.author);
    setCategory(book.category || "");
  };

  const handleCancelEdit = () => {
    setEditing(null);
    setTitle("");
    setAuthor("");
    setCategory("");
    setCoverImage(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-gray-500">Loading books...</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      <h2 className="text-2xl font-bold">Manage Books</h2>

      <form onSubmit={handleAddOrEdit} className="bg-white p-4 rounded shadow space-y-4">
        <h3 className="font-semibold">{editing ? "Edit Book" : "Add New Book"}</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Title *</label>
            <input 
              type="text" 
              placeholder="Book Title" 
              className="w-full border px-3 py-2 rounded"
              value={title} 
              onChange={e => setTitle(e.target.value)}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm text-gray-600 mb-1">Author *</label>
            <input 
              type="text" 
              placeholder="Author Name" 
              className="w-full border px-3 py-2 rounded"
              value={author} 
              onChange={e => setAuthor(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Category</label>
            <input 
              type="text" 
              placeholder="Category" 
              className="w-full border px-3 py-2 rounded"
              value={category} 
              onChange={e => setCategory(e.target.value)}
            />
          </div>
          
          <div>
            <label className="block text-sm text-gray-600 mb-1">
              {editing ? "Cover Image (leave empty to keep current)" : "Cover Image"}
            </label>
            <input 
              type="file" 
              accept="image/*"
              className="w-full border px-3 py-2 rounded"
              onChange={e => setCoverImage(e.target.files[0])}
            />
          </div>
        </div>

        <div className="flex space-x-4">
          <Button type="submit">{editing ? "Update Book" : "Add Book"}</Button>
          {editing && (
            <Button type="button" onClick={handleCancelEdit} className="bg-gray-500">
              Cancel
            </Button>
          )}
        </div>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {books.map(book => (
          <motion.div 
            key={book.id}
            className="bg-white shadow rounded p-2 cursor-pointer hover:scale-105 transition-transform"
            whileHover={{ scale: 1.05 }}
          >
            <img 
              src={book.cover_image ? `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${book.cover_image}` : "/placeholder-book.svg"} 
              alt={book.title}
              className="w-full h-32 object-cover rounded mb-2"
              onError={(e) => { e.target.src = "/placeholder-book.svg"; }}
            />
            <h3 className="font-semibold text-sm truncate">{book.title}</h3>
            <p className="text-xs text-gray-500">{book.author}</p>
            {book.category && <p className="text-xs text-gray-400">{book.category}</p>}
            <div className="mt-2 flex space-x-2">
              <Button onClick={() => handleEdit(book)} className="bg-yellow-500 text-xs py-1">
                Edit
              </Button>
              <Button onClick={() => handleDelete(book.id)} className="bg-red-500 text-xs py-1">
                Delete
              </Button>
            </div>
          </motion.div>
        ))}
      </div>

      {books.length === 0 && !loading && (
        <p className="text-center text-gray-500">No books found. Add some books to get started.</p>
      )}
    </div>
  );
}

