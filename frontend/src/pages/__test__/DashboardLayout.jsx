import React from "react";

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-4 flex flex-col">
        <h2 className="text-2xl font-bold text-blue-600 mb-6">YourLOGO</h2>
        <nav>
          <ul>
            <li className="mb-4"><a href="#" className="text-gray-700 hover:text-blue-600">Dashboard</a></li>
            <li className="mb-4"><a href="#" className="text-gray-700 hover:text-blue-600">Analytics</a></li>
            <li className="mb-4"><a href="#" className="text-gray-700 hover:text-blue-600">Reports</a></li>
            <li className="mb-4"><a href="#" className="text-gray-700 hover:text-blue-600">Settings</a></li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex flex-col flex-1">
        {/* Top Navbar */}
        <header className="bg-white shadow p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">Dashboard</h1>
          <button className="bg-blue-600 text-white px-4 py-2 rounded">Edit Dashboard</button>
        </header>

        {/* Dynamic Content Area */}
        <main className="flex-1 p-6 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;