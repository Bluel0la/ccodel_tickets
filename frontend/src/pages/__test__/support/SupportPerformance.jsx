import { FiClock, FiCheckCircle, FiAlertTriangle, FiBarChart2, FiTrendingUp, FiUsers } from "react-icons/fi";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from "recharts";

const SupportPerformance = () => {
  const stats = [
    { title: "Total Tickets Handled", value: 245, icon: <FiBarChart2 size={28} /> },
    { title: "Resolved Tickets", value: 210, icon: <FiCheckCircle size={28} /> },
    { title: "Pending Tickets", value: 35, icon: <FiAlertTriangle size={28} /> },
    
  ];
const stats2 = [{ title: "High-Priority Tickets Resolved", value: 18, icon: <FiTrendingUp size={28} /> },
    { title: "Resolution Rate", value: "85%", icon: <FiCheckCircle size={28} /> },
    { title: "Tickets Escalated", value: 12, icon: <FiAlertTriangle size={28} /> },
    { title: "Pending vs Resolved Tickets", value: "35 / 210", icon: <FiBarChart2 size={28} /> },]
  const topAgents = [
    { name: "John Doe", ticketsResolved: 50 },
    { name: "Sarah Smith", ticketsResolved: 45 },
    { name: "Michael Lee", ticketsResolved: 40 },
  ];

  const ticketTrends = [
    { month: "Jan", resolved: 40, pending: 10 },
    { month: "Feb", resolved: 50, pending: 15 },
    { month: "Mar", resolved: 55, pending: 20 },
    { month: "Apr", resolved: 60, pending: 25 },
  ];

  const ticketBreakdown = [
    { name: "Technical Issues", value: 100, color: "#3b4794" },
    { name: "Billing", value: 60, color: "#3179bc" },
    { name: "General Inquiry", value: 85, color: "#e6c5b1" },
  ];

  return (
    <div className="px-6 pb-6 transition-all duration-300 w-full grid grid-cols-1 md:grid-cols-6 gap-6">
      {/* Stats Cards */}
      {stats.map((stat, index) => (
        <div key={index} className="p-6 bg-[#3b4794] text-white border border-gray-200 rounded-lg shadow-sm flex flex-col justify-center items-center md:col-span-[1.5]">
          <div className="p-3 bg-white text-[#3b4794] rounded-full mb-2">{stat.icon}</div>
          <h5 className="text-2xl font-bold tracking-tight">{stat.value}</h5>
          <p className="mt-2 text-lg font-semibold text-center">{stat.title}</p>
        </div>
      ))}
           {stats2.map((stat, index) => (
        <div key={index} className="p-6 bg-[#3b4794] text-white border border-gray-200 rounded-lg shadow-sm flex flex-col justify-center items-center md:col-span-[1.5]">
          <div className="p-3 bg-white text-[#3b4794] rounded-full mb-2">{stat.icon}</div>
          <h5 className="text-2xl font-bold tracking-tight">{stat.value}</h5>
          <p className="mt-2 text-lg font-semibold text-center">{stat.title}</p>
        </div>
      ))}

      {/* Ticket Trends Chart */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm md:col-span-6">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Trends</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={ticketTrends}>
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="resolved" stroke="#28a745" strokeWidth={2} />
            <Line type="monotone" dataKey="pending" stroke="#ff4d4f" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Ticket Categories Breakdown */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm md:col-span-3">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Categories Breakdown</h2>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={ticketBreakdown} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value">
              {ticketBreakdown.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Top Performing Agents */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm md:col-span-3">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Top Performing Agents</h2>
        <ul className="space-y-4">
          {topAgents.map((agent, index) => (
            <li key={index} className="flex items-center justify-between p-3 border-b">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-[#3b4794] font-bold">
                  {agent.name.split(" ").map((n) => n[0]).join("")}
                </div>
                <span className="text-gray-700 font-semibold">{agent.name}</span>
              </div>
              <span className="text-sm text-gray-600">{agent.ticketsResolved} Tickets Resolved</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SupportPerformance;
