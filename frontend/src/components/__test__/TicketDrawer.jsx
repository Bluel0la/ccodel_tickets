import { FiX } from "react-icons/fi";
import { useEffect } from "react";

const TicketDrawer = ({ isOpen, onClose, ticket }) => {
  useEffect(() => {
    // Prevent scrolling when the drawer is open
    if (isOpen) {
      document.body.classList.add("overflow-hidden");
    } else {
      document.body.classList.remove("overflow-hidden");
    }
    return () => document.body.classList.remove("overflow-hidden");
  }, [isOpen]);

  return (
    <>
      {/* Backdrop with correct behavior (Clicking it closes the drawer) */}
      <div
        className={`fixed inset-0 bg-white bg-opacity-20 z-40 transition-opacity ${isOpen ? "visible opacity-100" : "invisible opacity-0"}`}
        onClick={onClose}
      ></div>

      {/* Drawer (Slides in from the right) */}
      <div
        className={`fixed top-0 right-0 z-50 h-screen w-80 md:w-96 bg-white shadow-lg transform transition-transform ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 bg-[#3b4794] text-white">
          <h5 className="text-lg font-semibold">Ticket Details</h5>
          <button onClick={onClose} className="p-2 rounded-full hover:bg-[#2e3a77] transition">
            <FiX size={22} />
          </button>
        </div>

        {/* Ticket Details */}
        <div className="p-5 space-y-4">
          {ticket ? (
            <>
              <p className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">Ticket ID:</span> {ticket.id}
              </p>
              <p className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">User:</span> {ticket.user}
              </p>
              <p className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">Category:</span> {ticket.subject}
              </p>
              <p className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">Priority:</span>
                <span className={`ml-2 px-2 py-1 rounded-md text-xs font-medium ${
                  ticket.priority === "High" ? "bg-red-100 text-red-500" : 
                  ticket.priority === "Medium" ? "bg-yellow-100 text-yellow-500" : 
                  "bg-green-100 text-green-500"
                }`}>
                  {ticket.priority}
                </span>
              </p>
              <p className="text-sm text-gray-600">
                <span className="font-semibold text-gray-900">Status:</span>
                <span className={`ml-2 px-2 py-1 rounded-md text-xs font-medium ${
                  ticket.status === "Open" ? "bg-red-100 text-red-500" : 
                  ticket.status === "Pending" ? "bg-yellow-100 text-yellow-500" : 
                  "bg-green-100 text-green-500"
                }`}>
                  {ticket.status}
                </span>
              </p>
              <div>
                <p className="text-sm text-gray-600 font-semibold">Description:</p>
                <p className="text-gray-700 bg-gray-100 p-3 rounded-md mt-1 text-sm">
                  {ticket.description || "No description provided."}
                </p>
              </div>
            </>
          ) : (
            <p className="text-gray-500 text-sm">No ticket selected.</p>
          )}
        </div>
      </div>
    </>
  );
};

export default TicketDrawer;
