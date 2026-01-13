import { createContext, useState, useEffect, useContext } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedUser = localStorage.getItem("user");
      const token = localStorage.getItem("access_token");
      
      if (storedUser && token) {
        try {
          setUser(JSON.parse(storedUser));
          // Optionally verify token is still valid
          const res = await api.get("auth/me/");
          setUser(res.data);
          localStorage.setItem("user", JSON.stringify(res.data));
        } catch (err) {
          // Token invalid, clear storage
          console.log("Token invalid, logging out");
          logout();
        }
      }
      setLoading(false);
    };
    
    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await api.post("auth/login/", { email, password });
    localStorage.setItem("access_token", res.data.access);
    localStorage.setItem("refresh_token", res.data.refresh);
    
    const userRes = await api.get("auth/me/");
    localStorage.setItem("user", JSON.stringify(userRes.data));
    setUser(userRes.data);
    return userRes.data;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setUser(null);
  };

  const refreshToken = async () => {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) {
      logout();
      return false;
    }
    
    try {
      const res = await api.post("auth/refresh/", { refresh });
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
      return true;
    } catch (err) {
      logout();
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, refreshToken, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

