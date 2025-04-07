import { Link, useLocation } from "react-router-dom";
import { FiHome, FiMessageSquare, FiBarChart2, FiSettings, FiUsers, FiFileText, FiClipboard, FiFolder, FiPieChart } from "react-icons/fi";
import logo from "../../assets/logo.png"
import logo_mini from '../../assets/logo-mini.png'
const Navbar = ({ isOpen, toggleNavbar }) => {
  const location = useLocation();

  // Extract role from URL (e.g., /test/admin/dashboard → "admin")
  const match = location.pathname.match(/^\/test\/(admin|student|support)\//);
  const role = match ? match[1] : null;

  const pages = {
    admin: [
      { name: "Dashboard", path: "/test/admin/dashboard", icon: <FiHome size={20} /> },
      { name: "Manage Students", path: "/test/admin/student-management", icon: <FiUsers size={20} /> },
      { name: "Manage Tickets", path: "/test/admin/tickets", icon: <FiClipboard size={20} /> },
      { name: "Categories", path: "/test/admin/categories", icon: <FiFolder size={20} /> },
      { name: "Reports", path: "/test/admin/reports", icon: <FiPieChart size={20} /> },
      { name: "Settings", path: "/test/admin/settings", icon: <FiSettings size={20} /> },
    ],
    student: [
      { name: "Dashboard", path: "/test/student/dashboard", icon: <FiHome size={20} /> },
      { name: "Create Ticket", path: "/test/student/tickets/new-ticket", icon: <FiFileText size={20} /> },
      { name: "My Tickets", path: "/test/student/tickets", icon: <FiClipboard size={20} /> },
      { name: "Knowledge Base", path: "/test/student/knowledge-base", icon: <FiFolder size={20} /> },
    ],
    support: [
      { name: "Dashboard", path: "/test/support/dashboard", icon: <FiHome size={20} /> },
      { name: "Assigned Tickets", path: "/test/support/tickets", icon: <FiClipboard size={20} /> },
      { name: "Knowledge Base", path: "/test/support/knowledge-base", icon: <FiFolder size={20} /> },
      { name: "Performance Reports", path: "/test/support/reports", icon: <FiBarChart2 size={20} /> },
      { name: "Settings", path: "/test/support/settings", icon: <FiSettings size={20} /> },
    ],
  };

  const links = role ? pages[role] : [];

  return (
    <div
      className={`fixed top-0 left-0 h-full transition-all duration-500 ease-in-out z-50 ${
        isOpen ? "w-64" : "w-16"
      } bg-gray-900 text-white shadow-lg`}
    >
      {/* Navbar Header */}
      <div className={`p-4 flex ${isOpen? "flex-row":"flex-col"} items-center justify-between transition-all duration-500 ease-in-out`}>
        {isOpen ? <h1 className="text-xl font-bold"><img src={logo} className="transition-all duration-500 ease-in-out"/></h1>:<h1 className="text-xl font-bold"><img src={logo_mini} className="transition-all duration-500 ease-in-out"/></h1>}
        <button className="text-white p-2 transition-all duration-500 ease-in-out" onClick={toggleNavbar}>
          {isOpen ? "✖" : "☰"}
        </button>
      </div>

      {/* Navigation */}
      <nav className="mt-4 flex flex-col items-center">
        {links.length > 0 ? (
          links.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`flex items-center p-3 w-full rounded-md transition-all duration-500 ease-in-out ${
                location.pathname === link.path ? "bg-pink-500" : "hover:bg-gray-700"
              } ${isOpen ? "justify-start space-x-4 pl-4" : "justify-center"}`}
            >
              <span className="text-sm transition-all duration-500 ease-in-out">{link.icon}</span>
              {isOpen && <span className="text-base transition-all duration-500 ease-in-out">{link.name}</span>}
            </Link>
          ))
        ) : (
          <p className="p-3 text-gray-400 transition-all duration-500 ease-in-out">Role not found</p>
        )}
      </nav>
    </div>
  );
};

export default Navbar;