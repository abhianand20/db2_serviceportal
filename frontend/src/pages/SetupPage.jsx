// src/pages/SetupPage.jsx
import { useState } from "react";
import { useAppContext } from "../context/AppContext";

function SetupPage() {
  const {configure} = useAppContext();

  const [server, setServer] = useState("localhost");
  const [instance, setInstance] = useState("db2inst1");
  const [dbName, setDbName] = useState("testdb");
  

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!server || !instance || !dbName) return;
  console.log(e)
    configure(server, instance, dbName);
  };

  return (
    <div style={{
      // width: "100%",
      // maxWidth: "900px",
      // padding: "24px",
      // borderRadius: "12px",
      // boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
      // display: "flex",
      // flexDirection: "column",
      // gap: "16px",
      // backgroundColor: "#f9f9f9",
      // fontFamily: "Arial, sans-serif",
      // display: "flex",
      // justifyContent: "center",   // horizontal center
      // alignItems: "center",  
      display: "flex",
      justifyContent: "center",
      alignItems: "center",

      width: "100%"     // vertical center
   
    
    }}
  >
<form 
  onSubmit={handleSubmit} 
  style={{
    width: "100%",
    maxWidth: "600px",
    padding: "24px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    gap: "16px",
    backgroundColor: "#f9f9f9",
    fontFamily: "Arial, sans-serif"
  }}
>
  <h2 style={{ textAlign: "center", margin: 0, marginBottom: "12px" }}>
    Welcome to DB2 Service Portal Setup
  </h2>

  <input
    placeholder="Server Name"
    value={server}
    onChange={(e) => setServer(e.target.value)}
    required
    style={{
      padding: "10px",
      borderRadius: "6px",
      border: "1px solid #ccc",
      fontSize: "14px"
    }}
  />

  <input
    placeholder="Instance Name"
    value={instance}
    onChange={(e) => setInstance(e.target.value)}
    required
    style={{
      padding: "10px",
      borderRadius: "6px",
      border: "1px solid #ccc",
      fontSize: "14px"
    }}
  />

  <input
    placeholder="Database Name"
    value={dbName}
    onChange={(e) => setDbName(e.target.value)}
    required
    style={{
      padding: "10px",
      borderRadius: "6px",
      border: "1px solid #ccc",
      fontSize: "14px"
    }}
  />

  <button
    type="submit"
    style={{
      padding: "10px",
      borderRadius: "6px",
      border: "none",
      backgroundColor: "#1e90ff",
      color: "white",
      fontSize: "16px",
      cursor: "pointer",
      transition: "background-color 0.2s",
    }}
    onMouseOver={e => (e.target.style.backgroundColor = "#1c86ee")}
    onMouseOut={e => (e.target.style.backgroundColor = "#1e90ff")}
  >
    Continue
  </button>
</form>

</div>

  );
}

// 🔑 Make sure default export is present
export default SetupPage;
