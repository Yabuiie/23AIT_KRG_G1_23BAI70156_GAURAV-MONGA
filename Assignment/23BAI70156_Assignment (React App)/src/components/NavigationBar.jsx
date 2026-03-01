import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

function Navigationbar() {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) return null;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/dashboard/water">Water Tracker</Link>
      <button onClick={handleLogout}>Logout</button>
    </nav>
  );
}

export default Navigationbar;