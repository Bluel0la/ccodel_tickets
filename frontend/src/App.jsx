import "./App.css";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Dashboard from "./pages/student/Dashboard";
import TestAdminDash from "./pages/__test__/admin/TestAdminDash";
function App() {
  return (
    <Routes>
      {/*Auth Routes  I'm testing here, don't be scared*/}
      <Route path="/" element={<Login />} />
      <Route path='/register' element={<Register/>}/>
      <Route path='/test/admin' element={<Register/>}/>
      <Route path='/test/student/dashboard' element={<TestAdminDash/>}/>
      <Route path='/test/support/dashboard' element={<TestAdminDash/>}/>
      <Route path='/test/admin/dashboard' element={<TestAdminDash/>}/>
      <Route path='/regi' element={<Register/>}/>
      <Route path='/ster' element={<Register/>}/>
      <Route path='/er' element={<Register/>}/>
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
