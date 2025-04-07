import { useState, useEffect } from "react";
import { FiUserX, FiSearch } from "react-icons/fi";

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    // Fetch students from API
    fetch("/api/students")
      .then((res) => res.json())
      .then((data) => setStudents(data))
      .catch((error) => console.error("Error fetching students:", error));
  }, []);

  const handleDeactivate = (id) => {
    // Deactivate student account
    fetch(`/api/students/${id}/deactivate`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        setStudents((prev) =>
          prev.map((student) =>
            student.id === id ? { ...student, active: false } : student
          )
        );
      })
      .catch((error) => console.error("Error deactivating student:", error));
  };

  const filteredStudents = students.filter((student) =>
    student.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Student Management</h2>
      <div className="flex items-center mb-4">
        <FiSearch className="text-gray-500 mr-2" />
        <input
          type="text"
          placeholder="Search students..."
          className="p-2 border rounded w-full"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Name</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Status</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredStudents.map((student) => (
            <tr key={student.id} className="text-center">
              <td className="border p-2">{student.name}</td>
              <td className="border p-2">{student.email}</td>
              <td className={`border p-2 ${student.active ? "text-green-500" : "text-red-500"}`}>
                {student.active ? "Active" : "Inactive"}
              </td>
              <td className="border p-2">
                {student.active && (
                  <button
                    onClick={() => handleDeactivate(student.id)}
                    className="flex items-center bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
                  >
                    <FiUserX className="mr-2" /> Deactivate
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentManagement;