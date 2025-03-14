import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom"
import Property from "../../components/student/Propertitybar";

const Createticket = ({ onCreate }) => {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [category, setCategory] = useState("");
    const [priority, setPriority] = useState("");


  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() || !description.trim() || !category || !priority) return;

    const newTicket = {
        id: Date.now(), // Unique ID for the ticket
        title,
        description,
        category,
        priority, // Store priority level
        status: "Pending", // Default status
        createdAt: new Date().toISOString(),
      };

      
    // Call the function passed from the parent component to add the ticket
      onCreate(newTicket);

      setTitle("");
      setDescription("");
      setCategory("");
      setPriority("");
      // Navigate back to dashboard after creating
    navigate("/home");
};

    return (
        <div>
            <Property />
            <div class=" sm:ml-64">
                <div class=" border-2 bg-[#bacbef]  text-white border-gray-200 h-187  rounded-lg dark:border-gray-700 ">
                    <div className="max-w-2xl mx-auto mt-25 p-6 bg-white text-black rounded-lg shadow-lg">
                        <h1 className="text-2xl font-bold mb-2">Need Assistance?</h1>
                        <p className="mb-6 text-sm">Please fill out the form below to create a ticket. Our team will get back to you soon.</p>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            {/* Issue Title */}
                            <div>
                                <label className="block mb-1 font-semibold">Issue Title</label>
                                <input
                                     type="text"
                                     name="title"
                                     className="w-full p-2 border rounded-md"
                                     placeholder="Enter issue title..."
                                     value={title}
                                     onChange={(e) => setTitle(e.target.value)}
                                     required
                                />
                            </div>

                            {/* Description */}
                            <div>
                                <label className="block text-sm font-semibold mb-2">Description</label>
                                <textarea
                                     className="w-full p-2 border rounded-md"
                                     rows="3"
                                     placeholder="Describe your issue..."
                                     value={description}
                                     onChange={(e) => setDescription(e.target.value)}
                                     required
                                ></textarea>
                            </div>

                            {/* Category Select */}
                            <div>
                                <label className="block text-sm font-semibold mb-2">Category</label>
                                <select
                                     name="category"
                                     value={category}
                                     onChange={(e) => setCategory(e.target.value)}
                                     className="w-full p-2 border rounded-md"
                                     required
                                >
                                    <option value="">Select Category</option>
                                    <option value="academic">Academic</option>
                                    <option value="it">IT</option>
                                    <option value="personal">Personal</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            {/* Priority Select */}
                            <div>
                                <label className="block text-sm font-semibold mb-2">Priority</label>
                                <select
                                     name="priority"
                                     value={priority}
                                     onChange={(e) => setPriority(e.target.value)}
                                     className="w-full p-2 border rounded-md"
                                     required
                                >
                                    <option value="">Select Priority</option>
                                    <option value="high">High</option>
                                    <option value="medium">Medium</option>
                                    <option value="low">Low</option>
                                </select>
                            </div>

                            {/* Submit Button */}
                            <div className="flex justify-start">
                                <button type="submit" onClick={() => navigate("/home")} className="mt-4 px-6 py-3 bg-blue-600  text-white rounded-md hover:bg-[#bacbef] hover:text-black">
                                    Submit Ticket
                                </button>
                            </div>
                        </form>
                    </div>

                </div>

            </div>
        </div>
    )
}
export default Createticket