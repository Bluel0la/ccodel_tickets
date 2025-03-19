import React from "react";
import { Link } from "react-router-dom"
import Property from "../../components/student/Propertitybar";
const Dashboard = () => {

  return (
    <div>
      <Property />
      <div class=" sm:ml-64">
        <div class=" border-2  bg-[#bacbef] text-white border-gray-200 h-187  rounded-lg dark:border-gray-700 ">
          <div class="flex flex-col gap-5 items-center text-black justify-center h-24 mt-80 rounded-sm dark:bg-gray-800 w-full">
            <h1 class="font-bold text-xl text-black md:text-2xl lg:text-5xl">
              Welcome to
            </h1>
            <h2 className="font-bold lg:text-3xl ">
              Your Support Ticket System
            </h2>
            <div className="mt-20 text-center">
              <p className="font-bold md:text-xl">What you can do here:</p>
              <div className="mt-3 flex justify-center gap-5">
                <Link to="/Create">
                  <button type="button" className="px-5 py-3 w-60 h-30 text-base font-medium text-center text-white bg-[#3b4794]  rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-[#bacbef] dark:focus:ring-blue-800">

                    Log a complaint
                  </button>
                </Link>
                <Link to="/home">
                  <button type="button" className="px-5 py-3 w-60 h-30 text-base font-medium text-center text-white bg-[#3b4794] rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-[#3b4794] dark:focus:ring-blue-800">

                    Track your ticket
                  </button>
                </Link>
                <Link to="/inbox">
                  <button type="button" className="px-5 py-3 w-60 h-30 text-base font-medium text-center text-white bg-[#3b4794] rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                  Check Notifications</button>
                </Link>

              </div>
            </div>

          </div>





        </div>
      </div>

    </div>
  );
};

export default Dashboard;
