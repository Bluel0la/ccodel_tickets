import { FiClipboard, FiUsers, FiAlertTriangle, FiClock } from "react-icons/fi";

const AdminDashboard = ({ isNavbarOpen }) => {
  const stats = [
    { title: "Open Tickets", value: 45, description: "Waiting for response", icon: <FiClipboard size={28} /> },
    { title: "Active Users", value: 1_230, description: "Currently online", icon: <FiUsers size={28} /> },
    { title: "Urgent Tickets", value: 8, description: "High priority pending", icon: <FiAlertTriangle size={28} /> },
    { title: "Avg. Response Time", value: "2h 15m", description: "Support response time", icon: <FiClock size={28} /> },
  ];

  return (
    <div
      className={`px-6 pb-6 transition-all duration-300 w-full ${
        isNavbarOpen ? "lg:ml-64 md:ml-16 sm:ml-16" : "ml-2"
      }`}
    >


      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-5">
        {stats.map((stat, index) => (
          <div key={index} className="p-6 bg-[#3b4794] text-white border border-gray-200 rounded-lg shadow-sm">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-white text-[#3b4794] rounded-full">{stat.icon}</div>
              <h5 className="text-2xl font-bold tracking-tight">{stat.value}</h5>
            </div>
            <p className="mt-2 text-lg font-semibold">{stat.title}</p>
            <p className="text-sm text-white/80">{stat.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;
