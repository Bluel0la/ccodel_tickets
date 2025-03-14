import React, { useState } from "react";
import Property from "../../components/student/Propertitybar";


const Inbox = () => {
    const [selectedMessage, setSelectedMessage] = useState(null);
    const messages = [
        { id: 1, ticketTitle: "Login Complaint", response: "Your issue has been resolved.", status: "Resolved" },
        { id: 2, ticketTitle: "Pending complaint", response: "We are looking into this.", status: "Pending" },
        { id: 3, ticketTitle: "Feature Request", response: "Thank you for your suggestion!", status: "Open" },
    ];
    return (
        <div>
            <Property />
            <div class=" sm:ml-64">
                <div className="border-2 bg-[#bacbef] text-white p-5 border-gray-200 h-188  rounded-lg dark:border-gray-700">
                    <h1 className="font-bold mt-20 text-4xl text-black">Inbox</h1>

                    <div className="flex flex-col gap-6">
                        {/* Messages List */}
                        <div className="mt-10 bg-white  rounded-sm border-gray-300 pr-4">
                           
                            <ul>
                                {messages.map((msg) => (
                                    <li
                                        key={msg.id}
                                        className={`p-3 text-blue-500 cursor-pointer border-b border-gray-300 transition duration-300 rounded-md ${selectedMessage?.id === msg.id
                                                ? "bg-blue-100 text-blue-700 font-semibold"
                                                : "hover:bg-gray-100"
                                            }`}
                                        onClick={() => setSelectedMessage(msg)}
                                    >
                                        <p className="font-semibold">{msg.ticketTitle}</p>
                                        <p className="text-sm text-gray-600">{msg.status}</p>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Message Detail View */}
                        <div className="col-span-2 p-6 bg-gray-100  rounded-lg shadow-md">
                            {selectedMessage ? (
                                <div>
                                    <h2 className="text-2xl text-black font-bold">{selectedMessage.ticketTitle}</h2>
                                    <p className="text-gray-600">{selectedMessage.status}</p>
                                    <div className="mt-4 p-4 bg-green-100 border border-green-300 rounded-md">
                                        <p className="font-semibold text-green-800">Support Reply:</p>
                                        <p className="text-lg text-gray-800">{selectedMessage.response}</p>
                                    </div>
                                    {selectedMessage.status === "Resolved" && (
                                        <div className="mt-4 p-4 bg-green-200 border border-green-400 rounded-md">
                                            <p className="text-green-900">✅ Your issue has been resolved successfully! If you need further assistance, feel free to contact us.</p>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <p className="text-gray-600">Select a ticket to view the response.</p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Inbox