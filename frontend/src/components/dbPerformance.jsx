import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { useAppContext } from "../context/AppContext";
import  { Card, DetailedSec } from "./MainCards";
// optional




function DbPerformance() {
  const { server, instance, dbName } = useAppContext();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [activeCard, setActiveCard] = useState(null);



  const fetchPerformance = () => {
    setError(null);
    setData(null);

    apiGet(server, instance, dbName, "/performance")
      .then((res) => {
        console.log("API response:", res);
        setData(res);
      })
      .catch((err) => {
        console.error("API error:", err);
        setError(err.message);
      });
  };


  useEffect(() => {
    fetchPerformance();
  }, [server, instance, dbName]);



  if (error) return <p style={{ color: "red" }}>Performance Error: {error}</p>;
  if (!data) return <p>Loading Performance Data...</p>;


  const cardsData = [
    { Title: "Package Hit Ratio", data: data.pkg_cache_hit_ratio, Message: "No Package Cache" },
    { Title: "Catalog Hit Ratio", data: data.cat_cache_hit_ratio, Message: "No Catalog Cache" },
    { Title: "Deadlocks", data: data.deadlocks, Message: "No Deadlocks" },
    { Title: "Long Running Query", data: data.longrunning_query_data, Message: "No Long Running Queries" },
    { Title: "Bufferpool Hit Ratio", data: data.buffer_pool_data, Message: "Data Not Available" },
    { Title: "Lock-wait", data: data.locking_data, Message: "No Lock-wait" },
    { Title: "Top 5 High Read Tables", data: data.table_rows_read, Message: "No High Read Tables" },
    { Title: "Top 5 Table Read Efficiency", data: data.table_read_efficiency, Message: "No Table Read Efficiency" },
    { Title: "Top 5 High CPU Queries", data: data.high_cpu_query, Message: "No High CPU Queries" },
    { Title: "Top 5 Frequent Queries", data: data.frequent_queries, Message: "No Frequent Queries" },
    { Title: "Top 5 Queries doing sort", data: data.top_sort_queries, Message: "No Queries doing sort" },
    { Title: "Top 5 Problematic Queries", data: data.problematic_queries, Message: "No Problematic Queries" },
    { Title: "Top 5 Queries consuming Temp TBSP", data: data.temp_table_queries, Message: "No Queries consuming Temp TBSP" }
  ];
  

  return (


<div style={{width:"100%",padding:"16px"}}>


  <button
          onClick={fetchPerformance}
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
          🔄 Click to Refresh
        </button>

<div   style={{
  width:"100%",
  padding:"10px",
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",  // center horizontally
    alignItems: "stretch",
    gap: "16px",
    flexWrap: "wrap",  
    boxSizing:"border-box"        // wrap on small screens
  }}>




 {cardsData.map((card) => (
<div style={{
  flex: "0 0 250px",
  gap:"40 px",
  maxWidth:"160px"
}}>


{/* <Card   
key={card.Title}
Title={card.Title}
isActive={activeCard===card.Title}
onToggle={() => setActiveCard(activeCard === card.Title ? null : card.Title)}
/>  */}

{ (activeCard===card.Title) && !Array.isArray(card.data)  ?
 ( <DetailedSec 
  key={card.Title}
  Title={card.Title}
  Message={card.Message}
  data={card.data}
  isActive={activeCard===card.Title}/>) : (
    <Card   
    key={card.Title}
    Title= {(activeCard===card.Title)? "Scroll down to see Data" : card.Title}
    isActive={activeCard===card.Title}
    onToggle={() => setActiveCard(activeCard === card.Title ? null : card.Title)}
    /> 
  )}



  </div>



 ))}

 </div>

<div style={{textAlign:"center"}}> <h3> *************************************************************************************************************************************************************</h3></div>
{cardsData.map(
  (card) => 
 activeCard === card.Title && Array.isArray(card.data) &&(
  <DetailedSec 
  key={card.Title}
  Title={card.Title}
  Message={card.Message}
  data={card.data}
  isActive={activeCard===card.Title}
  />)

)}


</div>

  );
}

export default DbPerformance;
