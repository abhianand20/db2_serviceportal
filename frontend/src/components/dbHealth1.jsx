import { useAppContext } from "../context/AppContext";
import  { Card, DetailedSec } from "./MainCards"
import { useEffect,useState } from "react";
import { apiGet } from "../api/client";

function DbHealth(){
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [activeCard, setActiveCard] = useState(null);
  const { server, instance, dbName } = useAppContext();
  const [showAll, setShowAll] = useState(false);

  function fetchHealth() {

    setData(null);
    apiGet(server, instance, dbName, "/healthcheck")
    .then((res) => {
      console.log("API response:", res);
      setData(res);
    })
    .catch((err) => {
      console.error("API error:", err);
      setError(err.message);
    });
  }

    useEffect(() => {

      fetchHealth();
    }, [server, instance, dbName]);

    if (error) return <p style={{ color: "red" }}>Health Error: {error}</p>;
    if (!data) return <p>Loading DB Health...</p>;





    const cardsData = [
      { Title: "DB NAME", data: data.database_name, Message: "NOT FOUND" },
      { Title: "DB Member No.", data: data.member, Message: "NOT FOUND" },
      { Title: "Start Time", data: data.db2_start_time, Message: "DB Start Time" },
      { Title: "DB Activation Status", data: data.activation_state, Message: "NOT FOUND" },
      { Title: "DB Connection Time:", data: data.connection_time, Message: "NOT FOUND" },
      { Title: "No of lock-waits:", data: data.num_locks_waiting, Message: "No Lock wait" },
      { Title: "No of lock escals:", data: data.lock_escals, Message: "No Lock escalation" },
      { Title: "No of lock-timeouts", data: data.lock_timeouts, Message: "No lock-timeouts" },
        { Title: "DB Memory(used)", data: data.DB_Memory, Message: "No Data" },
        { Title: "Log Utilisation", data: data.log_utilisation, Message: "No Data" },
        { Title: "DB Connection Status", data: data.database_connection, Message: "DB Connection:Failed" },
        { Title: "DB Status", data: data.db_status, Message: "No Data" },
        { Title: "Lastest Full Backup", data: data.last_full_backup, Message: "No Lastest Full Backup" },
        { Title: "Lastest INC Backup", data: data.inc_backup_data, Message: "No Lastest INC Backup" },
        { Title: "Lastest Delta Backup", data: data.del_backup_data, Message: "No Lastest Delta Backup" },
        { Title: "Container Status", data: data.container_status, Message: "All Containers are accesible" },
        { Title: "Tablestates Status", data: data.tablespace_issues, Message: "All Tablespaces Normal" },
        { Title: "Tables Status", data: data.table_issues, Message: "All Tables Normal" },
        { Title: "HADR Status", data: data.hadr_status, Message: "HADR: Not Configured" },
        { Title: "Load Pending Tables", data: data.loadpending_tables, Message: "No Load Pending Tables" },
        { Title: "Reorg Pending Tables", data: data.reorgpending_tables, Message: "No Reorg Pending Tables" },
        { Title: "Index Rebuild Status", data: data.indexrebuildpending_tables, Message: "No Index for rebuild" },
        { Title: "Invalid Views", data: data.invalid_views, Message: "No Invalid Views" },
        { Title: "Invalid Packages", data: data.invalid_packages, Message: "No Invalid Pakcages" },
        { Title: "Invalid_objects", data: data.invalid_objects, Message: "No Invalid Objects" },
        { Title: "Invalid Triggers", data: data.invalid_triggers, Message: "No Invalid Triggers" },
        { Title: "Event Monitors", data: data.eventmonitor_err, Message: "No Event Monitors" },     
        { Title: "Tables without Primary key", data: data.table_no_pk, Message: "No Tables without Primary key" },
        { Title: "DB Utilities", data: data.utilities, Message: "No Utility Running" }

      ];
      

return(<div style={{ padding:"16px",width:"100%"}}>
      <h2>DB2 Diagnostic Logs for last 24 hours</h2>  
        <div style={{
            display:"flex",
            flexDirection:"row",
            justifyContent:"space-between",
            alignItems:"center",
            marginBottom:"12px"
        }}>


<button
          onClick={fetchHealth}
          style={{
            marginBottom: "16px",
            padding: "8px 16px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#1e90ff",
            color: "#fff",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          🔄  Refresh
        </button>


        <button
  onClick={() => setShowAll((prev) => !prev)}
  style={{
    marginBottom: "16px",
    padding: "8px 16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#1e90ff",
    color: "#fff",
    cursor: "pointer",
    fontWeight: "bold",
  }}
>
  {showAll ? "Hide All Details" : "Show All Details"}
</button>

        </div>

                    <div
        style={{
            width:"100%",
            padding:"10px",
              display: "flex",
              flexDirection: "row",
              justifyContent: "center",  
              alignItems: "stretch",
              gap: "16px",
              flexWrap: "wrap",  
              boxSizing:"border-box" 
    
        }}
        > 
        
        {/* {cardsData.map((card)=>(
            <div style={{
            flex: "0 0 10px",
            gap:"40 px",
            maxWidth:"160px",
            textAlign:"center",
            justifyContent:"center"
            }}>
     
            <Card 
            key={card.Title}
            Title={card.Title}
            isActive={activeCard===card.Title}
            onToggle={() => setActiveCard(activeCard === card.Title ? null : card.Title)}
            />  
       </div>   

    
        
      

        ))} */}


{cardsData.map((card) => (
<div style={{
  flex: "0 0 250px",
  gap:"40 px",
  maxWidth:"160px"
}}>



{ (card.Title=="database_name" || (activeCard===card.Title && !Array.isArray(card.data)))  ?
 ( <DetailedSec 
  key={card.Title}
  Title={card.Title}
  Message={card.Message}
  data={card.data}
  isActive={activeCard===card.Title}/>) : ((
    <Card   
    key={card.Title}
    Title= {(activeCard===card.Title)? "Scroll down to see Data" : card.Title}
    isActive={activeCard===card.Title}
    onToggle={() => setActiveCard(activeCard === card.Title ? null : card.Title)}
    /> 
  ))}



  </div>



 ))}


 

  

        </div>

        <div
        style={{
            margin:"24px",
        }}  
        >
                 
 
       {cardsData.map((card)=>(
        
        (showAll || activeCard===card.Title) && Array.isArray(card.data)  && ( <DetailedSec 
        key={card.Title}
        Title={card.Title}
        data={card.data}
        Message={card.Message}
        isActive={activeCard===card.Title}
        />
      
      )   

        ))}

        </div>






        <div
             style={{
                width: "100%",
                display: "flex",
                flexDirection: "row",
                gap: "16px",
                flexWrap: "wrap",
                boxSizing: "border-box",
                justifyContent:"center"
              }}
>
    
  {cardsData.map(
    (card) =>
      (showAll) &&
      !Array.isArray(card.data) && (
        <div
        style={{
            width:"200px",
            maxWidth:"250px"

        }}
   
        
        >
            
        <DetailedSec
          key={card.Title}
          Title={card.Title}
          data={card.data}
          Message={card.Message}
          isActive={activeCard === card.Title}
        />
        </div>
      )
  )}
</div>












</div>);


}


export default DbHealth;
