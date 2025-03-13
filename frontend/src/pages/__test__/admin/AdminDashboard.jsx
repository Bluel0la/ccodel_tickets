import { useState } from "react";
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { FiClipboard, FiUsers, FiAlertTriangle, FiClock } from "react-icons/fi";
import TicketTable from "../../../components/__test__/TicketTable";
import TicketDrawer from "../../../components/__test__/TicketDrawer";

const AdminDashboard = ({ isNavbarOpen }) => {
  const tickets = [
    { id: "#1012", user: "John Doe", subject: "Login Issue", status: "Open", priority: "High", date: "March 12" },
    { id: "#1013", user: "Sarah Smith", subject: "Payment Failure", status: "Pending", priority: "Medium", date: "March 11" },
    { id: "#1014", user: "Mark Lee", subject: "Course Enrollment Bug", status: "Resolved", priority: "Low", date: "March 10" },
  ];
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const handleViewTicket = (ticket) => {
    setSelectedTicket(ticket);
    setIsDrawerOpen(true);
  };

  const stats = [
    { title: "Open Tickets", value: 45, description: "Waiting for response", icon: <FiClipboard size={24} /> },
    { title: "Active Users", value: 1_230, description: "Currently online", icon: <FiUsers size={24} /> },
    { title: "Urgent Tickets", value: 8, description: "High priority pending", icon: <FiAlertTriangle size={24} /> },
    { title: "Avg. Response Time", value: "2h 15m", description: "Support response time", icon: <FiClock size={24} /> },
  ];

  const ticketCategories = [
    { name: "Technical Issues", value: 50, color: "#3b4794" },
    { name: "Billing", value: 30, color: "#3179bc" },
    { name: "Course Enrollment", value: 20, color: "#e6c5b1" },
  ];

  const ticketTrends = [
    { month: "Jan", open: 40, resolved: 20 },
    { month: "Feb", open: 55, resolved: 30 },
    { month: "Mar", open: 60, resolved: 50 },
    { month: "Apr", open: 70, resolved: 65 },
    { month: "May", open: 80, resolved: 75 },
  ];

  return (
    <div
      className={`px-4 pb-6 transition-all duration-300 w-full ${
        isNavbarOpen ? "lg:ml-64 md:ml-16 sm:ml-16" : "lg:ml-6 ml-2"
      }`}
    >

      {/* Stats Cards */}
      <div className="grid align-center  justify-center grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 my-6 md:w-[90vw] w-[77vw]">
        {stats.map((stat, index) => (
          <div key={index} className="p-4 bg-[#3b4794] text-white border border-gray-200 rounded-lg shadow-sm">
            <div className="flex items-center space-x-4">
              <div className="p-2 bg-white text-[#3b4794] rounded-full">{stat.icon}</div>
              <h5 className="text-lg sm:text-2xl font-bold tracking-tight">{stat.value}</h5>
            </div>
            <p className="mt-1 text-base font-semibold">{stat.title}</p>
            <p className="text-sm text-white/80">{stat.description}</p>
          </div>
        ))}
      </div>

      {/* Ticket Categories & Ticket Trends (Responsive Grid) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6 md:w-[90vw]  w-[77vw]">
        <div className="bg-white p-4 sm:p-6 border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-lg sm:text-xl font-semibold text-[#3b4794] mb-4">Ticket Categories Breakdown</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={ticketCategories} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value" label>
                {ticketCategories.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-4 sm:p-6 border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-lg sm:text-xl font-semibold text-[#3b4794] mb-4">Ticket Trends</h2>
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

      {/* Recent Tickets Table (Responsive) */}
      <div className="bg-white p-4 sm:p-6 border border-gray-200 rounded-lg shadow-sm mb-6 md:w-[90vw]  w-[77vw]">
        <h2 className="text-lg sm:text-xl font-semibold text-[#3b4794] mb-4">Recent Tickets</h2>
        <TicketTable tickets={tickets} onViewTicket={handleViewTicket} />

{/* Drawer */}
<TicketDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} ticket={selectedTicket} />
      </div>
    </div>
  );
};

export default AdminDashboard;
