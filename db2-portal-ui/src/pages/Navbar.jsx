import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav
      style={{
        display: "flex",
        gap: "24px",
        padding: "12px 24px",
        background: "#0f172a",
        color: "white",
        width: "100%",
      }}
    >
      <Link style={linkStyle} to="/">Home</Link>
      <Link style={linkStyle} to="/dbsummary">DB-Summary</Link>
      <Link style={linkStyle} to="/health">DB-Health</Link>
      <Link style={linkStyle} to="/performance">DB-Performance</Link>
      <Link style={linkStyle} to="/diaglog">DiagLog</Link>
    </nav>
  );
}

const linkStyle = {
  color: "white",
  textDecoration: "none",
  fontWeight: "500",
};

export default Navbar;
