// app/components/NavBar.jsx
import { Link, useNavigate, useLocation } from "@remix-run/react";
import { useState, useEffect } from "react";

export default function NavBar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, [location.pathname]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    navigate("/login");
  };

  // Styles for improved navbar design
  const navBarStyle = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    height: "60px",
    background: "linear-gradient(90deg, #66a6ff, #89f7fe)",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 2rem",
    zIndex: 1000,
  };

  const logoStyle = {
    fontSize: "1.5rem",
    fontWeight: "bold",
    color: "#fff",
    textDecoration: "none",
    display: "flex",
    alignItems: "center",
  };

  const navLinksStyle = {
    display: "flex",
    alignItems: "center",
  };

  const linkStyle = {
    color: "#fff",
    textDecoration: "none",
    marginLeft: "1.5rem",
    fontSize: "1rem",
    fontWeight: "500",
  };

  const buttonStyle = {
    background: "none",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    marginLeft: "1.5rem",
    fontSize: "1rem",
    fontWeight: "500",
  };

  return (
    <nav style={navBarStyle}>
      <Link to="/dashboard" style={logoStyle}>
        🚀 Portfolio Analyzer
      </Link>
      <div style={navLinksStyle}>
        {isLoggedIn ? (
          <>
            <Link to="/dashboard" style={linkStyle}>
              Dashboard
            </Link>
            <button onClick={handleLogout} style={buttonStyle}>
              Logout
            </button>
          </>
        ) : (
          <>
            {location.pathname !== "/login" && (
              <Link to="/login" style={linkStyle}>
                Login
              </Link>
            )}
            {location.pathname !== "/register" && (
              <Link to="/register" style={linkStyle}>
                Register
              </Link>
            )}
          </>
        )}
      </div>
    </nav>
  );
}
