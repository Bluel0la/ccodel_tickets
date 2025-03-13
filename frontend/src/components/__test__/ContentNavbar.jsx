import { useState } from "react";
import { useLocation } from "react-router-dom";
import { FiChevronDown } from "react-icons/fi";

const ContentNavbar = () => {
  const location = useLocation();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Extract page name from URL
  const pageTitle = location.pathname
    .split("/")
    .filter(Boolean)
    .slice(-1)[0]
    .replace(/-/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase()) || "Dashboard";

  return (
    <div className="flex justify-between items-center px-6 py-4 bg-white shadow-sm">
      {/* Page Title */}
      <h1 className="text-2xl font-bold text-[#3b4794] font-['Merriweather']">
        {pageTitle}
      </h1>

      {/* User Dropdown */}
      <div className="relative">
        <button
          onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          className="flex items-center space-x-2 cursor-pointer"
        >
          <div class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-gray-100 rounded-full dark:bg-gray-600">
    <span class="font-medium text-gray-600 dark:text-gray-300">JL</span>
</div>
          <FiChevronDown className="text-gray-600" />
        </button>

        {/* Dropdown Menu */}
        {isDropdownOpen && (
          <div className="absolute right-0 mt-2 w-44 bg-white divide-y divide-gray-100 rounded-lg shadow-sm">
            <div className="px-4 py-3 text-sm text-gray-900">
              <div>Bonnie Green</div>
              <div className="font-medium truncate">name@flowbite.com</div>
            </div>
            <ul className="py-2 text-sm text-gray-700">
              <li>
                <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                  Dashboard
                </a>
              </li>
              <li>
                <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                  Settings
                </a>
              </li>
              <li>
                <a href="#" className="block px-4 py-2 hover:bg-gray-100">
                  Earnings
                </a>
              </li>
            </ul>
            <div className="py-1">
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Sign out
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ContentNavbar;
