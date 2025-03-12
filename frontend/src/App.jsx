import "./App.css";
import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Dashboard from "./pages/student/Dashboard";
import DashContainer from "./pages/__test__/DashContainer";
function App() {
  return (
    <Routes>
      {/*Auth Routes */}
      <Route path="/" element={<Login />} />
      <Route path='/register' element={<Register/>}/>
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
