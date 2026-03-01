import { Link, Outlet } from "react-router-dom";
import Navbar from "./Navbar";

function Layout() {
  return (
    <>
      {/* NAVBAR */}
      <Navbar/>

      {/* PAGE CONTENT GOES HERE */}
      <Outlet />
    </>
  );
}

export default Layout;
