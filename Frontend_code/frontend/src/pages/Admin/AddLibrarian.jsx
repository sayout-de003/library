import { useState } from "react";
import api from "../../services/api";
import Button from "../../components/Button";

export default function AddLibrarian() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await api.post("auth/add-librarian/", { email, username, password });
      alert("Librarian added successfully");
      setEmail(""); setUsername(""); setPassword("");
    } catch (err) {
      alert("Failed to add librarian");
    }
  };

  return (
    <div className="p-4 flex justify-center">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow space-y-4 w-80">
        <h2 className="text-xl font-bold">Add Librarian</h2>
        <input placeholder="Username" className="w-full border px-2 py-1 rounded" value={username} onChange={e => setUsername(e.target.value)} />
        <input placeholder="Email" className="w-full border px-2 py-1 rounded" value={email} onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" className="w-full border px-2 py-1 rounded" value={password} onChange={e => setPassword(e.target.value)} />
        <Button type="submit">Add Librarian</Button>
      </form>
    </div>
  );
}
