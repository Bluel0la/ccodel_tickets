const TicketTable = ({ tickets }) => {
    return (
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th className="px-4 py-2">Title</th>
              <th className="px-4 py-2">Priority</th>
              <th className="px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((ticket) => (
              <tr key={ticket.id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2">{ticket.subject}</td>
                <td className={`px-4 py-2 ${ticket.priority === "High" ? "text-red-500" : ticket.priority === "Medium" ? "text-yellow-500" : "text-green-500"}`}>
                  {ticket.priority}
                </td>
                <td className="px-4 py-2">
                  <button className="text-blue-600 hover:underline">View</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };
  
  export default TicketTable;
  