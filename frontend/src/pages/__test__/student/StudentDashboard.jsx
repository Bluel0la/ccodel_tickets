import { FiBook, FiClipboard, FiCheckCircle, FiPlusCircle, FiLifeBuoy, FiClock , FiPlus} from "react-icons/fi";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import TicketTable from "../../../components/__test__/TicketTable";
import { Link } from "react-router-dom";

const StudentDashboard = () => {

  const tickets = [
    { id: "#2015", subject: "Lecture Notes Missing", status: "Open", priority: "Medium", date: "March 14" },
    { id: "#2016", subject: "Course Registration Issue", status: "Resolved", priority: "High", date: "March 13" },
    { id: "#2017", subject: "Exam Date Change", status: "Pending", priority: "Low", date: "March 12" },
  ];

  const stats = [
    { title: "Open Tickets", value: 2, description: "Issues awaiting response", icon: <FiClipboard size={28} /> },
    { title: "Resolved Tickets", value: 5, description: "Successfully closed cases", icon: <FiCheckCircle size={28} /> },
    { title: "Total Tickets", value: 12, description: "All-time submissions", icon: <FiBook size={28} /> },
    { title: "Create New Ticket", description: "", icon: <Link to="/test/student/tickets/new"><FiPlus size={28} /></Link> },
  ];

  const ticketTrends = [
    { month: "Jan", open: 5, resolved: 2 },
    { month: "Feb", open: 7, resolved: 4 },
    { month: "Mar", open: 6, resolved: 5 },
    { month: "Apr", open: 3, resolved: 2 },
  ];

  const knowledgeBaseLinks = [
    { title: "How to Reset Your Password", link: "#" },
    { title: "Fixing Login Issues", link: "#" },
    { title: "Contacting Support", link: "#" },
  ];

  const supportHours = [
    { day: "Monday - Friday", hours: "9:00 AM - 6:00 PM" },
    { day: "Saturday", hours: "10:00 AM - 3:00 PM" },
    { day: "Sunday", hours: "Closed" },
  ];



  return (
    <div className="px-6 pb-6 transition-all duration-300 w-full bg-gradient-to-r from-blue-400 to-purple-500">

      {/* Stats Cards + Create New Ticket Button */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 py-6 md:w-[90vw]  w-[77vw]">
      {stats.map((stat, index) => (
          <div key={index} className="p-4 bg-[#3b4794] text-white rounded-lg shadow-sm flex  flex-col items-center justify-center">
            <div className="flex items-center space-x-4">
              <div className="p-2 bg-white text-[#3b4794] rounded-full">{stat.icon}</div>
              <h5 className="text-lg sm:text-2xl font-bold tracking-tight">{stat.value}</h5>
            </div>
            <p className="mt-1 text-base font-semibold font-['Merriweather']">{stat.title}</p>
            <p className="text-sm text-white/80">{stat.description}</p>
          </div>
        ))}
        
        </div>
     

      {/* Knowledge Base & Support Hours */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6 md:w-[90vw]  w-[77vw]">
        {/* Knowledge Base */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm ">
          <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Knowledge Base</h2>
          <ul className="space-y-2">
            {knowledgeBaseLinks.map((kb, index) => (
              <li key={index}>
                <a href={kb.link} className="text-blue-600 hover:underline flex items-center space-x-2">
                  <FiLifeBuoy size={16} />
                  <span>{kb.title}</span>
                </a>
              </li>
            ))}
          </ul>
          <a href="#" className="mt-4 inline-block text-blue-600 font-semibold hover:underline">
            View All Articles
          </a>
        </div>

        {/* Live Support Hours */}
        <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm ">
          <h2 className="text-xl font-semibold text-[#3b4794] mb-4 flex items-center space-x-2">
            <FiClock size={20} />
            <span>Live Support Hours</span>
          </h2>
          <ul className="space-y-2">
            {supportHours.map((day, index) => (
              <li key={index} className="flex justify-between">
                <span className="text-gray-700">{day.day}</span>
                <span className="text-gray-900 font-medium">{day.hours}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Ticket Trends Chart */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm mb-6 md:w-[90vw]  w-[77vw]">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Support Ticket Trends</h2>
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

      {/* Ticket Table (At Bottom) */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm overflow-x-auto md:w-[90vw]  w-[77vw]">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Recent Support Tickets</h2>
        <TicketTable tickets={tickets} />
      </div>
    </div>
  );
};

export default StudentDashboard;
