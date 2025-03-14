import { useState } from "react";
import { FiClipboard, FiCheckCircle, FiClock, FiUserCheck, FiAlertTriangle, FiPlusCircle, FiFilter, FiBell, FiUsers } from "react-icons/fi";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from "recharts";
import TicketTable from "../../../components/__test__/TicketTable";

const SupportDashboard = () => {
  const [isCreatingTicket, setIsCreatingTicket] = useState(false);
  const [ticketDetails, setTicketDetails] = useState({ subject: "", description: "" });
  const [ticketFilter, setTicketFilter] = useState("All");

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

  const ticketOverview = [
    { name: "Open", value: 20, color: "#ff4d4f" },
    { name: "Pending", value: 10, color: "#ffc107" },
    { name: "Resolved", value: 85, color: "#28a745" },
  ];

  const notifications = [
    {
      message: "New ticket assigned to you: #3045",
      type: "ticket",
      time: "2 mins ago",
    },
    {
      message: "Ticket #3012 marked as Resolved",
      type: "ticket",
      time: "1 hour ago",
    },
    {
      message: "Admin posted a new announcement",
      type: "announcement",
      time: "Yesterday",
    },
   
  ];
  
  const teamActivity = [
    { name: "Sarah Adams", task: "Handling Ticket #3015", status:" Online" },
    { name: "James Davies", task: "Resolved 3 tickets today",status:" Online" },
    { name: "Linda Kren", task: "Working on ticket #3018" ,status:" Online"},
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
     
      </div>

      {/* Ticket Overview + Response Time + Notifications */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {/* Ticket Overview (Pie Chart) */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Status Overview</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={ticketOverview} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value">
                {ticketOverview.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Recent Notifications */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
  <h2 className="text-xl font-semibold text-[#3b4794] mb-4 flex items-center">
    <FiBell className="mr-2" /> Recent Notifications
  </h2>
  <ul className="space-y-4">
    {notifications.map((note, index) => (
      <li key={index} className="flex items-center justify-between border-b pb-3">
        {/* Notification Icon & Message */}
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-gray-100 rounded-full">
            {note.type === "ticket" ? (
              <FiClipboard className="text-blue-600" />
            ) : note.type === "announcement" ? (
              <FiUsers className="text-green-600" />
            ) : (
              <FiAlertTriangle className="text-red-600" />
            )}
          </div>
          <span className="text-gray-700">{note.message}</span>
        </div>
        {/* Timestamp */}
        <span className="text-xs text-gray-500">{note.time}</span>
      </li>
    ))}
  </ul>
</div>

        {/* Support Team Activity */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
  <h2 className="text-xl font-semibold text-[#3b4794] mb-4 flex items-center">
    <FiUsers className="mr-2" /> Support Team Activity
  </h2>
  <ul className="space-y-4">
    {teamActivity.map((member, index) => (
      <li key={index} className="flex items-center justify-between border-b pb-2">
        {/* Avatar */}
        <div className="flex items-center space-x-3">
          <div className="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-gray-100 rounded-full">
            <span className="font-medium text-gray-600">
              {member.name.split(" ").map(n => n[0]).join("")}
            </span>
          </div>
          <span className="text-gray-700 font-medium">{member.name}</span>
        </div>
        {/* Task and Status */}
        <div className="flex items-center space-x-3">
          <span className="text-gray-600">{member.task}</span>
          <span className={`px-2 py-1 text-xs font-semibold rounded-lg ${member.status === "Online" ? "bg-green-100 text-green-600" : "bg-gray-300 text-gray-700"}`}>
            {member.status}
          </span>
        </div>
      </li>
    ))}
  </ul>
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
    </div>
  );
};

export default SupportDashboard;
