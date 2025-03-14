import { useState } from "react";
import { Link } from "react-router-dom"
import Property from "../../components/student/Propertitybar";
const Home = () => {



    const [tickets, setTickets] = useState([]);
    const totalTickets = tickets.length;
    const pendingTickets = tickets.filter((t) => t.status === "Pending").length;
    const resolvedTickets = tickets.filter((t) => t.status === "Resolved").length;

    const updateTicketStatus = (ticketId) => {
        setTickets((prevTickets) =>
            prevTickets.map((ticket) =>
                ticket.id === ticketId
                    ? { ...ticket, status: "Resolved", progress: 100 }
                    : ticket
            )
        );
    };


    return (
        <div>
            <Property />
            <div class=" sm:ml-64 mt-13 ">
                <div class=" border-2 bg-[#3b4794] bg-[#bacbef] text-white p-5 border-gray-200 h-175  rounded-lg dark:border-gray-700 ">

                    <h1 className="text-4xl font-bold  pt-10 text-gray-800 mb-4">Welcome! Need Help?</h1>
                    <p className=" text-black text-xl font-bold mb-6">Create  a ticket and check your progress below.</p>
                    <div className="flex justify-start">

                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-6">
                        <div className="bg-blue-700 text-white p-4 rounded-md shadow">
                            <p className="text-lg font-semibold">Total Tickets</p>
                            <p className="text-2xl">{totalTickets}</p>
                        </div>
                        <div className="bg-blue-700 text-white p-4 rounded-md shadow">
                            <p className="text-lg font-semibold">Pending</p>
                            <p className="text-2xl">{pendingTickets}</p>
                        </div>
                        <div className="bg-blue-700 text-white p-4 rounded-md shadow">
                            <p className="text-lg font-semibold">Resolved</p>
                            <p className="text-2xl">{resolvedTickets}</p>
                        </div>
                    </div>

                    {/* Ticket Progress Section */}
                    <h2 className="text-2xl  text-black font-bold mb-4">Ticket Progress</h2>
                    <div className="space-y-4">
                        {tickets.map((ticket) => (
                            <div key={ticket.id} className="p-4 border rounded-md shadow">
                                <p className="font-semibold">{ticket.title}</p>
                                <p className="text-sm text-gray-600">{ticket.status}</p>
                                {/* Progress Bar */}
                                <div className="w-full bg-gray-200 h-3 rounded-md mt-2">
                                    <div
                                        className={`h-3 rounded-md ${ticket.progress === 100 ? "bg-green-500" : "bg-blue-500"
                                            }`}
                                        style={{ width: `${ticket.progress}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Create Ticket Button */}
                    <Link to="/create">
                    <button className="absolute px-6 mt-70 ml-280 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                        Create Ticket
                    </button>
                </Link>
                </div>

                

            </div>


        </div>
    );
};

export default Home;
