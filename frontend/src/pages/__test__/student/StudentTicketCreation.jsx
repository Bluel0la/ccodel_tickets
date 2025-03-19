import { useState } from "react";
import { FiUpload, FiPaperclip, FiFileText, FiImage, FiVideo } from "react-icons/fi";

const StudentTicketCreation = () => {
  const [ticketDetails, setTicketDetails] = useState({
    subject: "",
    category: "",
    description: "",
    attachment: null,
    attachmentPreview: null,
  });
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTicketDetails({ ...ticketDetails, [name]: value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileType = file.type;
      let preview = null;

      if (fileType.startsWith("image")) {
        preview = URL.createObjectURL(file);
      } else if (fileType.startsWith("video")) {
        preview = URL.createObjectURL(file);
      } else if (fileType === "application/pdf") {
        preview = URL.createObjectURL(file);
      } else if (fileType.includes("officedocument") || fileType.includes("msword")) {
        preview = "doc";
      }

      setTicketDetails({ ...ticketDetails, attachment: file, attachmentPreview: preview });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsModalOpen(true);
    setTicketDetails({ subject: "", category: "", description: "", attachment: null, attachmentPreview: null });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-gradient-to-r from-blue-400 to-purple-500">
      {/* Ticket Form */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Create a New Ticket</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Subject</label>
            <input
              type="text"
              name="subject"
              value={ticketDetails.subject}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg mt-1"
              placeholder="Enter ticket subject"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Category</label>
            <select
              name="category"
              value={ticketDetails.category}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg mt-1"
              required
            >
              <option value="">Select a category</option>
              <option value="Technical Issue">Technical Issue</option>
              <option value="Billing">Billing</option>
              <option value="General Inquiry">General Inquiry</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              name="description"
              value={ticketDetails.description}
              onChange={handleChange}
              className="w-full p-2 border rounded-lg mt-1"
              placeholder="Describe your issue..."
              required
            ></textarea>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Attachment</label>
            <div className="flex items-center gap-3 border p-2 rounded-lg cursor-pointer hover:bg-gray-100 relative">
              <FiUpload className="text-gray-500" />
              <input type="file" accept="image/*,video/*,.pdf,.doc,.docx" onChange={handleFileChange} className="absolute inset-0 opacity-0 cursor-pointer" />
              <span className="text-gray-600">Upload a file</span>
            </div>
          </div>
          <button type="submit" className="bg-[#3b4794] text-white p-2 rounded-lg w-full hover:bg-[#2a356a]">
            Submit Ticket
          </button>
        </form>
      </div>

      {/* Attachment Preview */}
      <div className="bg-white p-6 border border-gray-200 rounded-lg shadow-sm flex flex-col items-center justify-center">
        <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Attachment Preview</h2>
        {ticketDetails.attachment ? (
          <div className="flex flex-col items-center w-full">
            {ticketDetails.attachment.type.startsWith("image") ? (
              <img src={ticketDetails.attachmentPreview} alt="Preview" className="max-w-full max-h-40 rounded-lg" />
            ) : ticketDetails.attachment.type.startsWith("video") ? (
              <video src={ticketDetails.attachmentPreview} controls className="max-w-full max-h-40 rounded-lg" />
            ) : ticketDetails.attachment.type === "application/pdf" ? (
              <iframe src={ticketDetails.attachmentPreview} className="w-full h-40 border rounded-lg" title="PDF Preview"></iframe>
            ) : (
              <FiPaperclip className="text-gray-500 text-3xl" />
            )}
            <p className="text-gray-700 mt-2">{ticketDetails.attachment.name}</p>
          </div>
        ) : (
          <p className="text-gray-500">No attachment uploaded</p>
        )}
      </div>

      {/* Success Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-[#ffffff99] bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg text-center w-96">
            <h2 className="text-xl font-semibold text-[#3b4794] mb-4">Ticket Submitted Successfully</h2>
            <p className="text-gray-600 mb-4">We'll get back to you as soon as possible.</p>
            <button
              onClick={() => setIsModalOpen(false)}
              className="bg-[#3b4794] text-white px-4 py-2 rounded-lg hover:bg-[#2a356a]"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentTicketCreation;
