import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logo from "../../assets/logo.png";
import { Link } from "react-router-dom";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!formData.email || !formData.password) {
      setError("All fields are required.");
      return;
    }

    if (!validateEmail(formData.email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        "https://ccodel-tickets.onrender.com/api/v1/auth/login",
        { email: formData.email, password: formData.password }
      );

      const { user, access_token, refresh_token } = response.data;
      sessionStorage.setItem("user_id", user?.userId || "");
      sessionStorage.setItem("role", user?.role || "");
      sessionStorage.setItem("access_token", access_token || "");
      sessionStorage.setItem("refresh_token", refresh_token || "");

      navigate(`/test/${user?.role}/dashboard`);
    } catch (error) {
      setError(
        error.response?.data?.message || "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-[#bacbef] px-4">
      <div className="w-full max-w-4xl flex flex-col md:flex-row shadow-lg rounded-lg overflow-hidden md:h-[90vh]">
        <div className="w-full md:w-1/2 bg-[#3b4794] text-white p-8 flex flex-col justify-center items-center md:items-start">
          <img src={logo} alt="Logo" />
          <p className="text-sm opacity-90 mb-6 text-center md:text-left font-[DM Sans]">
            Login to your student support portal to submit and track tickets.
          </p>
        </div>
        <div className="w-full md:w-1/2 bg-white p-8 flex flex-col justify-center">
          <h2 className="text-2xl font-bold text-[#3b4794] mb-2 text-center md:text-left font-[Merriweather]">
            Support Login
          </h2>
          <p className="text-sm text-gray-500 mb-6 text-center md:text-left font-[DM Sans]">
            Enter your credentials to access your support account.
          </p>
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              name="email"
              placeholder="Your Email"
              value={formData.email}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-[#3179bc] font-[DM Sans]"
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-[#3179bc] font-[DM Sans]"
            />
            <button
              type="submit"
              className="w-full bg-[#3b4794] hover:bg-[#3179bc] text-white font-bold p-3 rounded font-[DM Sans] flex justify-center items-center"
              disabled={loading}
            >
              {loading ? "Loading..." : "Login"}
            </button>
          </form>
          <p className="text-center text-sm text-gray-600 mt-4 font-[DM Sans]">
            Don't have an account? <Link to="/register" className="text-[#3179bc] hover:underline">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
