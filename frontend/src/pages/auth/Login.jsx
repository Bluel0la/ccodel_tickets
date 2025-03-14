import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import axios from "axios";
import logo from "../../assets/logo.png";
import { Link } from "react-router-dom";
import { Spinner } from "flowbite-react";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // Initialize navigate function

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(
        "https://ccodel-tickets.onrender.com/api/v1/auth/login",
        {
          email: formData.email,
          password: formData.password,
        }
      );

      alert("Login successful!");
      sessionStorage.setItem("user_id", response.data.user.userId);
      sessionStorage.setItem("role", response.data.user.role);
      // Navigate to the role-based dashboard
      navigate(`/test/${response.data.user.role}/dashboard`);
    } catch (error) {
      console.error("Login error:", error);
      alert("Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-[#bacbef] px-4">
      <div className="w-full max-w-4xl flex flex-col md:flex-row shadow-lg rounded-lg overflow-hidden md:h-[90vh]">
        {/* Left Section (Info Panel) */}
        <div className="w-full md:w-1/2 bg-[#3b4794] text-white p-8 flex flex-col justify-center items-center md:items-start">
          <img src={logo} />

          <p className="text-sm opacity-90 mb-6 text-center md:text-left font-[DM Sans]">
            Login to your student support portal to submit and track tickets.
          </p>
          <button className="bg-[#ffffff] hover:bg-[#e6c5b1] text-[#3b4794] px-4 py-2 rounded-md mb-3 w-full md:w-auto font-[DM Sans]">
            Learn More
          </button>
        </div>

        {/* Right Section (Login Form) */}
        <div className="w-full md:w-1/2 bg-white p-8 flex flex-col justify-center">
          <h2 className="text-2xl font-bold text-[#3b4794] mb-2 text-center md:text-left font-[Merriweather]">
            Support Login
          </h2>
          <p className="text-sm text-gray-500 mb-6 text-center md:text-left font-[DM Sans]">
            Enter your credentials to access your support account.
          </p>

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

            <div className="flex justify-between items-center mb-4">
              <label className="flex items-center text-sm text-gray-600 font-[DM Sans]">
                <input type="checkbox" className="mr-2" />
                Remember me
              </label>
              <a
                href="#"
                className="text-[#3179bc] text-sm hover:underline font-[DM Sans]"
              >
                Forgot Password?
              </a>
            </div>

            <button
              type="submit"
              className="w-full bg-[#3b4794] hover:bg-[#3179bc] text-white font-bold p-3 rounded font-[DM Sans] flex justify-center items-center"
              disabled={loading}
            >
              {loading ? <svg aria-hidden="true" className="w-8 h-8 text-white-200 animate-spin dark:text-white-600 fill-[#bacbef]" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
    </svg> : "Login"}
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-4 font-[DM Sans]">
            Don't have an account?{" "}
            <Link to="/register" className="text-[#3179bc] hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;