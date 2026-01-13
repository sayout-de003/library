// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://127.0.0.1:8000/api/",
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// api.interceptors.request.use(config => {
//   const token = localStorage.getItem("access_token");
//   if (token) config.headers.Authorization = `Bearer ${token}`;
//   return config;
// });

// export default api;

import axios from "axios";

const BASE_URL = "http://localhost:8000/api/"; // Use consistent base URL

const instance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add Authorization header if token exists
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
// Add after request interceptor
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        const res = await axios.post(`${BASE_URL}auth/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem("access_token", res.data.access);
        localStorage.setItem("refresh_token", res.data.refresh);
        originalRequest.headers["Authorization"] = `Bearer ${res.data.access}`;
        return instance(originalRequest);
      } catch (err) {
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);


export default instance;
