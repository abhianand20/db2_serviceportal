import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { useAppContext } from "../context/AppContext";

function DbDiagLog() {
  const { server, instance, dbName } = useAppContext();
  const [logs, setLogs] = useState(null);
  const [error, setError] = useState(null);

  function fetchdiaglog() {
    setLogs(null);

    Promise.all([
      apiGet(server, instance, dbName, "/db2diag/crit"),
      apiGet(server, instance, dbName, "/db2diag/err"),
      apiGet(server, instance, dbName, "/db2diag/warn"),
      apiGet(server, instance, dbName, "/db2diag/info")
    ])
      .then(([crit, err, warn, info]) => {
        setLogs({
          critical: crit.db2diag_crit || [],
          error: err.db2diag_err || [],
          warning: warn.db2diag_warn || [],
          info: info.db2diag_info || []
        });
        console.log(logs);
      })
      .catch((err) => setError(err.message));
  }


  useEffect(() => {
  fetchdiaglog();  
  }, [server, instance, dbName]);

  if (error) return <p style={{ color: "red" }}>Diag Error: {error}</p>;
  if (!logs) return <p>Loading DB2 Diagnostic Logs...</p>;

  return (
    <div>
      <h2>DB2 Diagnostic Logs for last 24 hours</h2>

      <button
          onClick={fetchdiaglog}
          style={{
            marginBottom: "16px",
            padding: "8px 16px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#1e90ff",
            color: "#fff",
            cursor: "pointer",
            fontWeight: "bold",
            width: "200px",
          }}
        >
          🔄  Refresh
        </button>
      
       {Object.entries(logs).map(([level, entries]) => (
        <div key={level}>
          <h3>Level : {level.toUpperCase()} </h3>
          {entries.length === 0 ? (
            <p>No entries for {level.toUpperCase()} alerts in last 24 hours</p>
          ) : (
            <table border="1">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>DBPARTITIONNUM</th>
                  <th>APPL_ID</th>
                  <th>SEV</th>
                  <th>MSGTYPE</th>
                  <th>MSGNUM</th>
                  <th>MSG_TRUNC</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((row, idx) => (
                  <tr key={idx}>
                    <td>{row.TIMESTAMP}</td>
                    <td>{row.DBPARTITIONNUM}</td>
                    <td>{row.APPL_ID_TRUNC}</td>
                    <td>{row.SEV}</td>
                    <td>{row.MSGTYPE}</td>
                    <td>{row.MSGNUM}</td>
                    <td>{row.MSG_TRUNC}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ))}
    </div>
  );
}

export default DbDiagLog;
