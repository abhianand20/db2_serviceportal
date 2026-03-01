import { Link, Outlet } from "react-router-dom";
import Navbar from "./Navbar";

function Layout() {
  return (
    <>
      {/* NAVBAR */}
      {/* <nav
        style={{
          padding: "12px",
          background: "#222",
          color: "white",
          display: "flex",
          gap: "16px",
        }}
      >
        <Link to="/" style={{ color: "white" }}>Home</Link>
        <Link to="/health" style={{ color: "white" }}>Health</Link>
        <Link to="/performance" style={{ color: "white" }}>Performance</Link>
        <Link to="/diaglog" style={{ color: "white" }}>Diag Log</Link>
        <Link to="/dbsummary" style={{ color: "white" }}>DB Summary</Link>
      </nav> */}
      <Navbar/>

      {/* PAGE CONTENT GOES HERE */}
      <Outlet />
    </>
  );
}

export default Layout;
