import { useState } from "react";
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { FiClipboard, FiUsers, FiAlertTriangle, FiClock, FiCheckCircle, FiBell } from "react-icons/fi";
import TicketTable from "../../../components/__test__/TicketTable";

const AdminDashboard = ({ isNavbarOpen }) => {
  const [ticketFilter, setTicketFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const tickets = [
    { id: "#1012", user: "John Doe", subject: "Login Issue", status: "Open", priority: "High", date: "March 12" },
    { id: "#1013", user: "Sarah Smith", subject: "Payment Failure", status: "Pending", priority: "Medium", date: "March 11" },
    { id: "#1014", user: "Mark Lee", subject: "Course Enrollment Bug", status: "Resolved", priority: "Low", date: "March 10" },
  ];
  const stats = [
    { title: "Open Tickets", value: 45, description: "Waiting for response", icon: <FiClipboard size={28} /> },
    { title: "Active Users", value: 1_230, description: "Currently online", icon: <FiUsers size={28} /> },
    { title: "Urgent Tickets", value: 8, description: "High priority pending", icon: <FiAlertTriangle size={28} /> },
    { title: "Avg. Response Time", value: "2h 15m", description: "Support response time", icon: <FiClock size={28} /> },
  ];

  // Ticket Categories Data for Pie Chart
  const ticketCategories = [
    { name: "Technical Issues", value: 50, color: "#3b4794" },
    { name: "Billing", value: 30, color: "#3179bc" },
    { name: "Course Enrollment", value: 20, color: "#e6c5b1" },
  ];

  // Ticket Trends Data for Line Chart
  const ticketTrends = [
    { month: "Jan", open: 40, resolved: 20 },
    { month: "Feb", open: 55, resolved: 30 },
    { month: "Mar", open: 60, resolved: 50 },
    { month: "Apr", open: 70, resolved: 65 },
    { month: "May", open: 80, resolved: 75 },
  ];

  return (
    <div
      className={`px-6 pb-6 transition-all duration-300 w-full ${
        isNavbarOpen ? "lg:ml-64 md:ml-16 sm:ml-16" : "ml"
      }`}
    >


      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 my-6 ">
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

      {/* Ticket Categories & Ticket Trends (Side by Side) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Ticket Category Breakdown (Pie Chart) */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Categories Breakdown</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={ticketCategories} cx="50%" cy="50%" innerRadius={60} outerRadius={80} dataKey="value" label>
                {ticketCategories.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Ticket Trends Chart (Line Chart) */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Trends</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={ticketTrends}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="open" stroke="#3179bc" strokeWidth={2} />
              <Line type="monotone" dataKey="resolved" stroke="#e6c5b1" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
       
      </div>
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm overflow-x-auto mb-6">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Recent Tickets</h2>
        <TicketTable tickets={tickets}/>
        </div>
    </div>
  );
};

export default AdminDashboard;
