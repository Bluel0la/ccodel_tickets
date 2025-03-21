import { useState } from "react";
import { FiSearch, FiChevronDown } from "react-icons/fi";
import TicketDrawer from "../../../components/__test__/TicketDrawer"; // Import the TicketDrawer component

const StudentTickets = ({ tickets }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState(null);
  const [dateFilter, setDateFilter] = useState("Last 30 days");
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);

  // Date Filter Options
  const dateFilters = ["Last day", "Last 7 days", "Last 30 days", "Last month", "Last year"];

  // Handle Sorting
  const handleSort = (field) => {
    setSortBy(field);
  };

  // Handle Opening the Drawer
  const handleViewTicket = (ticket) => {
    setSelectedTicket(ticket);
    setIsDrawerOpen(true);
  };

  // Apply Search & Sorting
  const filteredTickets = (tickets || [])
    .filter((ticket) => ticket.subject.toLowerCase().includes(searchQuery.toLowerCase()))
    .sort((a, b) => (sortBy ? (a[sortBy] > b[sortBy] ? 1 : -1) : 0));

  return (
    <div className="h-full relative overflow-x-auto shadow-md sm:rounded-lg p-4 bg-gradient-to-r from-blue-400 to-purple-500">
      {/* Search & Filter Controls */}
      <div className="flex flex-col sm:flex-row flex-wrap items-center justify-between pb-4 gap-4">
        {/* Date Filter Dropdown */}
        <div className="relative">
          <button className="inline-flex items-center text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 font-medium rounded-lg text-sm px-3 py-1.5">
            <FiChevronDown className="mr-2" />
            {dateFilter}
          </button>
        </div>

        {/* Search Bar */}
        <div className="relative w-full sm:w-auto">
          <FiSearch className="absolute left-3 top-2.5 text-gray-500" />
          <input
            type="text"
            placeholder="Search for tickets..."
            className="block w-full sm:w-80 p-2 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Table (Responsive) */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th className="p-4"></th>
              <th className="px-6 py-3 cursor-pointer" onClick={() => handleSort("id")}>Ticket ID</th>
              <th className="px-6 py-3 cursor-pointer" onClick={() => handleSort("subject")}>Category</th>
              <th className="px-6 py-3 cursor-pointer hidden md:table-cell" onClick={() => handleSort("status")}>Status</th>
              <th className="px-6 py-3 cursor-pointer hidden md:table-cell" onClick={() => handleSort("priority")}>Priority</th>
              <th className="px-6 py-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredTickets.length > 0 ? (
              filteredTickets.map((ticket) => (
                <tr key={ticket.id} className="border-b hover:bg-gray-50">
                  <td className="p-4">
                    <input type="checkbox" className="w-4 h-4 text-blue-600 border-gray-300 rounded" />
                  </td>
                  <td className="px-6 py-4">{ticket.id}</td>
                  <td className="px-6 py-4">{ticket.subject}</td>
                  <td className="px-6 py-4 hidden md:table-cell">
                    <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${
                      ticket.status === "Open" ? "bg-red-100 text-red-500" : 
                      ticket.status === "Pending" ? "bg-yellow-100 text-yellow-500" : 
                      "bg-green-100 text-green-500"
                    }`}>
                      {ticket.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 hidden md:table-cell">
                    <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${
                      ticket.priority === "High" ? "bg-red-100 text-red-500" : 
                      ticket.priority === "Medium" ? "bg-yellow-100 text-yellow-500" : 
                      "bg-green-100 text-green-500"
                    }`}>
                      {ticket.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button onClick={() => handleViewTicket(ticket)} className="text-blue-600 hover:underline">
                      View
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center py-4">No tickets found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Drawer Component */}
      <TicketDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} ticket={selectedTicket} />
    </div>
  );
};

export default StudentTickets;
