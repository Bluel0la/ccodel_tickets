import React, { useState } from "react";
import logo from "../../assets/logo.png";
import { Link } from "react-router-dom";

const Register = () => {
  const [formData, setFormData] = useState({ name: "", email: "", password: "", confirmPassword: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    alert("Registration successful!"); // Replace with actual registration logic
  };

  return (
    <div className="flex h-screen items-center justify-center bg-[#bacbef] px-4">
      <div className="w-full max-w-4xl flex flex-col md:flex-row shadow-lg rounded-lg overflow-hidden md:h-[90vh]">
        {/* Left Section (Info Panel) */}
        <div className="w-full md:w-1/2 bg-[#3b4794] text-white p-8 flex flex-col justify-center items-center md:items-start">
          <img src={logo} alt="CCODEL Logo" />
          <p className="text-sm opacity-90 mb-6 text-center md:text-left font-[DM Sans]">
            Register for the student support portal to submit and track tickets.
          </p>
          <button className="bg-[#ffffff] hover:bg-[#e6c5b1] text-[#3b4794] px-4 py-2 rounded-md mb-3 w-full md:w-auto font-[DM Sans]">
            Learn More
          </button>
        </div>

        {/* Right Section (Registration Form) */}
        <div className="w-full md:w-1/2 bg-white p-8 flex flex-col justify-center">
          <h2 className="text-2xl font-bold text-[#3b4794] mb-2 text-center md:text-left font-[Merriweather]">
            Support Registration
          </h2>
          <p className="text-sm text-gray-500 mb-6 text-center md:text-left font-[DM Sans]">
            Create an account to access the support system.
          </p>

          <form onSubmit={handleSubmit}>
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              value={formData.name}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-[#3179bc] font-[DM Sans]"
            />
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
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-[#3179bc] font-[DM Sans]"
            />

            <button
              type="submit"
              className="w-full bg-[#3b4794] hover:bg-[#3179bc] text-white font-bold p-3 rounded font-[DM Sans]"
            >
              Register
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-4 font-[DM Sans]">
            Already have an account? {" "}
            <Link to="/" className="text-[#3179bc] hover:underline">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
