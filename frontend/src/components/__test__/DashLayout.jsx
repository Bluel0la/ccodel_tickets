import React, { useState } from "react";
import Navbar from "./Navbar";
import AdminDashboard from "../../pages/__test__/admin/AdminDashboard";
import ContentNavbar from "./ContentNavbar";

const DashLayout = ({content}) => {
  const [isNavbarOpen, setIsNavbarOpen] = useState(false);

  return (
    <div className="flex overflow-x-hidden min-h-[100vh]">
   

      {/* Sidebar/Navbar */}
      <Navbar isOpen={isNavbarOpen} toggleNavbar={() => setIsNavbarOpen(!isNavbarOpen)} />

      <div className={`flex-1 transition-all duration-300 ${isNavbarOpen ? "lg:ml-16 md:ml-48 sm:ml-14" : "ml-14"}`}>
        <ContentNavbar />
        {content}
      </div>
    </div>
  );
};

export default DashLayout;
