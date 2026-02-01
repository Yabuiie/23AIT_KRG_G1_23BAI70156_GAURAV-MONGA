import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Header = () => {
    const {isAuthenticated} = useAuth();
    return (
        <header style = {{
            padding: '10px',
            backgroundColor: '#5499f8',
            color : 'white',
            textAlign: 'center',
        }}> 
            <h1>EcoTrack</h1>
            <Link to = "/">Dashboard</Link>{" "}
            <Link to = "/logs">Logs</Link>{" "}
            {isAuthenticated ? (
                <Link to = "/logout">Logout</Link>
            ) : (
                <Link to = "/login">Login</Link>
            )}
        </header> 
    )
}
export default Header;