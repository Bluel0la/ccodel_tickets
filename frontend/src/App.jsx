import "./App.css";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Dashboard from "./pages/student/Dashboard";
import TestAdminDash from "./pages/__test__/admin/TestAdminDash";
import DashLayout from "./components/__test__/DashLayout";
import AdminDashboard from "./pages/__test__/admin/AdminDashboard";
import StudentDashboard from "./pages/__test__/student/StudentDashboard";
import SupportDashboard from "./pages/__test__/support/SupportDashboard";
import SupportTickets from "./pages/__test__/support/SupportTickets";
import SupportPerformance from "./pages/__test__/support/SupportPerformance";
import Equation from "./pages/__test__/Equation";
function App() {
  return (
    <Routes>
      {/*Auth Routes  I'm testing here, don't be scared*/}
      <Route path="/" element={<Login />} />
      <Route path='/register' element={<Register/>}/>
      <Route path='/test/admin' element={<Register/>}/>
      <Route path='/test/student/dashboard' element={<DashLayout content={<StudentDashboard/>}/>}/>
      <Route path='/test/support/dashboard' element={<DashLayout content={<SupportDashboard/>}/>}/>
      <Route path='/test/admin/dashboard' element={<DashLayout content={<AdminDashboard/>}/>}/>
      <Route path='/test/support/tickets' element={<DashLayout content={<SupportTickets/>}/>}/>
      <Route path='/test/support/reports' element={<DashLayout content={<SupportPerformance/>}/>}/>
      <Route path='/test/' element={<Equation/>}/>
      <Route path='/ter' element={<Register/>}/>
      {/*Auth Routes */}

      {/*Admin Routes */}
        {/* <Route path='/admin' element={}/> */}
      {/*  <Route path='/admin' element={}/>*/}
      {/*  <Route path='/admin' element={}/>*/}
      {/*  <Route path='/admin' element={}/>*/}
      {/*  <Route path='/admin' element={}/>*/}
      {/*Admin Routes */}

      {/*Student Routes */}
        <Route path='/student' element={<Dashboard />}/>
      {/*  <Route path='student/' element={}/>*/}
      {/*  <Route path='student/' element={}/>*/}
      {/*  <Route path='student/' element={}/>*/}
      {/*  <Route path='student/' element={}/>*/}
      {/*  <Route path='student/' element={}/>*/}
      {/*Student Routes */}

      {/*Support Routes */}
      {/*  <Route path='/support' element={}/>*/}
      {/*  <Route path='/support' element={}/>*/}
      {/*  <Route path='/support' element={}/>*/}
      {/*  <Route path='/support' element={}/>*/}
      {/*  <Route path='/support' element={}/>*/}
      {/*  <Route path='/support' element={}/>*/}
      {/*Support Routes */}
    </Routes>
  );
}

export default App;
