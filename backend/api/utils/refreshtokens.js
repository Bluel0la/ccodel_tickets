import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true, // Important for refresh token
});

// Request interceptor to attach access token
api.interceptors.request.use(async (config) => {
  let token = localStorage.getItem("access_token");

  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }

  return config;
});

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response, 
  async (error) => {
    if (error.response?.status === 401) {
      try {
        // Attempt to refresh token
        const refreshResponse = await axios.post("http://localhost:8000/auth/refresh-token", {
          refresh_token: localStorage.getItem("refresh_token"),
        });

        localStorage.setItem("access_token", refreshResponse.data.access_token);

        // Retry original request with new token
        error.config.headers["Authorization"] = `Bearer ${refreshResponse.data.access_token}`;
        return axios(error.config);
      } catch (refreshError) {
        console.error("Refresh token expired. Logging out...");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login"; // Redirect to login
      }
    }

    return Promise.reject(error);
  }
);
