import React, { useState } from "react";
import logo from "../../assets/logo.png"
import {Link} from "react-router-dom"
const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Login successful!"); // Replace with actual authentication logic
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
              className="w-full bg-[#3b4794] hover:bg-[#3179bc] text-white font-bold p-3 rounded font-[DM Sans]"
            >
              Login
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
