import { useState } from "react";
import { FiClipboard, FiCheckCircle, FiClock, FiUserCheck, FiAlertTriangle, FiPlusCircle } from "react-icons/fi";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import TicketTable from "../../../components/__test__/TicketTable";

const SupportDashboard = () => {
  const [isCreatingTicket, setIsCreatingTicket] = useState(false);
  const [ticketDetails, setTicketDetails] = useState({ subject: "", description: "" });

  const tickets = [
    { id: "#3012", student: "Jane Doe", subject: "Account Locked", status: "Open", priority: "High", date: "March 14" },
    { id: "#3013", student: "Michael Smith", subject: "Email Verification Issue", status: "Pending", priority: "Medium", date: "March 13" },
    { id: "#3014", student: "Emily White", subject: "Reset Password", status: "Resolved", priority: "Low", date: "March 12" },
  ];

  const stats = [
    { title: "Open Tickets", value: 20, description: "Assigned to you", icon: <FiClipboard size={28} /> },
    { title: "Resolved Tickets", value: 85, description: "Cases successfully closed", icon: <FiCheckCircle size={28} /> },
    { title: "Pending Tickets", value: 10, description: "Awaiting response", icon: <FiAlertTriangle size={28} /> },
    { title: "Avg. Resolution Time", value: "3h 20m", description: "Time per resolved ticket", icon: <FiClock size={28} /> },
  ];

  const ticketTrends = [
    { month: "Jan", open: 15, resolved: 10 },
    { month: "Feb", open: 20, resolved: 15 },
    { month: "Mar", open: 25, resolved: 20 },
    { month: "Apr", open: 18, resolved: 16 },
  ];

  const handleCreateTicket = (e) => {
    e.preventDefault();
    console.log("New Ticket:", ticketDetails);
    setIsCreatingTicket(false);
    setTicketDetails({ subject: "", description: "" });
  };

  return (
    <div className="px-6 pb-6 transition-all duration-300 w-full">

      {/* Stats Cards + Create New Ticket Button */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 my-6">
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
        <div className="flex items-center justify-center">
          <button
            onClick={() => setIsCreatingTicket(true)}
            className="flex items-center space-x-2 px-6 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition w-full"
          >
            <FiPlusCircle size={20} />
            <span>Create New Ticket</span>
          </button>
        </div>
      </div>

      {/* Ticket Trends */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm mb-6">
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

      {/* Ticket Table */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm overflow-x-auto">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Assigned Tickets</h2>
        <TicketTable tickets={tickets} />
      </div>

      {/* Create New Ticket Form (Popup) */}
      {isCreatingTicket && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Submit a Support Ticket</h2>
            <form onSubmit={handleCreateTicket} className="space-y-4">
              <input
                type="text"
                placeholder="Subject"
                className="w-full p-2 border border-gray-300 rounded"
                value={ticketDetails.subject}
                onChange={(e) => setTicketDetails({ ...ticketDetails, subject: e.target.value })}
                required
              />
              <textarea
                placeholder="Describe the issue..."
                className="w-full p-2 border border-gray-300 rounded h-24"
                value={ticketDetails.description}
                onChange={(e) => setTicketDetails({ ...ticketDetails, description: e.target.value })}
                required
              />
              <div className="flex justify-between">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg">Submit</button>
                <button type="button" onClick={() => setIsCreatingTicket(false)} className="px-4 py-2 text-gray-600">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default SupportDashboard;
