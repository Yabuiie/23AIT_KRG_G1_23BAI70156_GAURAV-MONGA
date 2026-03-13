import { Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./routes/ProtectedRoute";

function App() {
    return (
        <>
        <Routes>
            <Route path = "/Login" element = {<Login/>} />\
            <Route path = "/" 
            element = {
                <ProtectedRoute>
                <Dashboard/>
                </ProtectedRoute>
            }></Route>
        </Routes>
        </>
    )
}
export default App;