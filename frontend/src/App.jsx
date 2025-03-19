import "./App.css";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from './pages/auth/Register'
import Dashboard from "./pages/student/Dashboard";
import Home from "./pages/student/Home";
import Createticket from "./pages/student/Createticket";
import TestAdminDash from "./pages/__test__/admin/TestAdminDash";
import DashLayout from "./components/__test__/DashLayout";
import AdminDashboard from "./pages/__test__/admin/AdminDashboard";
import StudentDashboard from "./pages/__test__/student/StudentDashboard";
import SupportDashboard from "./pages/__test__/support/SupportDashboard";
import SupportTickets from "./pages/__test__/support/SupportTickets";
import SupportPerformance from "./pages/__test__/support/SupportPerformance";
import Equation from "./pages/__test__/Equation";
import Inbox from "./pages/student/Inbox";
import StudentTicketCreation from "./pages/__test__/student/StudentTicketCreation";
import StudentTickets from "./pages/__test__/student/StudentTickets";
import KnowledgeBase from "./pages/student/KnowledgeBase";
function App() {
  return (
    <Routes>
      {/*Auth Routes  I'm testing here, don't be scared*/}
      <Route path="/" element={<Login />} />
      <Route path='/register' element={<Register/>}/>


      <Route path='/test/admin' element={<Register/>}/>
      <Route path='/test/admin/dashboard' element={<DashLayout content={<AdminDashboard/>}/>}/>


      <Route path='/test/support/dashboard' element={<DashLayout content={<SupportDashboard/>}/>}/>
      <Route path='/test/support/tickets' element={<DashLayout content={<SupportTickets/>}/>}/>
      <Route path='/test/support/reports' element={<DashLayout content={<SupportPerformance/>}/>}/>



      <Route path='/test/student/dashboard' element={<DashLayout content={<StudentDashboard/>}/>}/>
      <Route path='/test/student/tickets/new-ticket' element={<DashLayout content={<StudentTicketCreation/>}/>}/>
      <Route path='/test/student/tickets' element={<DashLayout content={<StudentTickets/>}/>}/>
      <Route path='/test/student/knowledge-base' element={<DashLayout content={<KnowledgeBase/>}/>}/>
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
       <Route path='/home' element={<Home/>}/>
      <Route path='/create' element={<Createticket/>}/>
        <Route path='/inbox' element={<Inbox/>}/>
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
