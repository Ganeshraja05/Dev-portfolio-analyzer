// app/routes/login.jsx
import { useState } from "react";
import { useNavigate } from "@remix-run/react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(window.ENV.API_URL + "/user/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const errData = await res.json();
        setError(errData.detail || "Login failed");
        return;
      }
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError("An error occurred during login.");
    }
  };

  const pageStyle = {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #89f7fe, #66a6ff)",
    padding: "1rem",
  };

  const cardStyle = {
    backgroundColor: "rgba(255, 255, 255, 0.95)",
    borderRadius: "12px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    padding: "2rem",
    width: "90%",
    maxWidth: "400px",
    textAlign: "center",
  };

  const titleStyle = {
    marginBottom: "1rem",
    fontSize: "2rem",
    color: "#333",
  };

  const labelStyle = {
    display: "block",
    marginBottom: "0.5rem",
    fontWeight: "bold",
    color: "#555",
    textAlign: "left",
  };

  const inputStyle = {
    width: "100%",
    padding: "0.75rem",
    marginBottom: "1rem",
    border: "1px solid #ccc",
    borderRadius: "6px",
    fontSize: "1rem",
  };

  const buttonStyle = {
    backgroundColor: "#66a6ff",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    cursor: "pointer",
    marginTop: "1rem",
    width: "100%",
  };

  const linkStyle = {
    color: "#66a6ff",
    textDecoration: "underline",
    cursor: "pointer",
  };

  return (
    <div style={pageStyle}>
      <div style={cardStyle}>
        <h2 style={titleStyle}>Welcome Back! 😃</h2>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <div>
            <label style={labelStyle}>Email 📧</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={inputStyle}
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label style={labelStyle}>Password 🔒</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={inputStyle}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" style={buttonStyle}>
            Login Now
          </button>
        </form>
        <p style={{ marginTop: "1rem", color: "#555" }}>
          Don't have an account?{" "}
          <span style={linkStyle} onClick={() => navigate("/register")}>
            Register here
          </span>
        </p>
      </div>
    </div>
  );
}
