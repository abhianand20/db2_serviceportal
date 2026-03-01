import DbSummaryPage from "./dbSummaryPage";
import SetupPage from "./SetupPage";
import { useAppContext } from "../context/AppContext";
function Dashboard() {
  const { isConfigured } = useAppContext();

  return (
    <div
      style={{
        width: "90%",
        maxWidth: "1600px",
        margin: "0 auto",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: "100px", fontSize: "35px", color: "", fontFamily:"Sans-serif" }}>
       DB2 Service Portal (Readonly Version)
      </h2>

      {isConfigured ? <DbSummaryPage /> : <SetupPage />}
    </div>
  );
}


export default Dashboard;
