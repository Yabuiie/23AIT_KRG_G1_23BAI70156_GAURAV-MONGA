import React from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Header = () => {
  const { isAuthenticated } = useAuth();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          sx={{ flexGrow: 1 }}
          data-testid="app-title"
        >
          EcoTrack
        </Typography>

        <Button
          color="inherit"
          component={Link}
          to="/"
          data-testid="dashboard-link"
        >
          Dashboard
        </Button>

        <Button
          color="inherit"
          component={Link}
          to="/logs"
          data-testid="logs-link"
        >
          Logs
        </Button>

        {isAuthenticated ? (
          <Button
            color="inherit"
            component={Link}
            to="/logout"
            data-testid="logout-link"
          >
            Logout
          </Button>
        ) : (
          <Button
            color="inherit"
            component={Link}
            to="/login"
            data-testid="login-link"
          >
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default React.memo(Header);