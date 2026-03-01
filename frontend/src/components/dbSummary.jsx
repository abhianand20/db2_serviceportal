import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import { useAppContext } from "../context/AppContext";
import SummaryCard from "./valueCard"
import TableCard from "./tableCard";

function DbSummary() {
  const { server, instance, dbName } = useAppContext();
  const [data, setData] = useState(null);


  
  useEffect(() => {
    setData(null);
    apiGet(server, instance, dbName, "/summary")
    .then((res) => {
      console.log("API response:", res);
      setData(res);
    })
    .catch((err) => {
      console.error("API error:", err);
      setError(err.message);
    });
  
  }, [server, instance, dbName]);


  if (!data) return <p>Loading DB Summary...</p>;

  return (
    <>
    
      <div>

   
    </div>
  

    <div style={{ display: "flex", gap: "4px", flexWrap: "wrap" }}>
  <SummaryCard label="Instance" value={data.instance_name} />
  <SummaryCard label="Database" value={data.database_name} />
  <SummaryCard label="DPF Enabled" value={data.is_dpf ? "Yes" : "No"} />
  <SummaryCard label="Partitions" value={data.Num_of_partitions} />
  <SummaryCard label="HADR" value={data.hadr_role="No Data"? "Not Configured":data.hadr_role} />
  <SummaryCard label="DB Status" value={data.db_status} />
  <SummaryCard label="DB Level" value={data.service_level} />
  <SummaryCard label="DB Size (GB)" value={data.database_size_gb} />
  <SummaryCard label="DB Size (MB)" value={data.database_size_mb} />
  <SummaryCard label="Last full backup" value={data.last_full_backup[0].start_date} />
  <SummaryCard  label="Last Inc backup" value={data?.inc_backup_data?.[0]?.start_date || "Not Available"}/>
  <SummaryCard label="Last Inc backup" value={data?.del_backup_data?.[0]?.start_date|| "Not Available"} />




</div>
    
    </>
    

    
  




  );
}

export default DbSummary;




// {Object.entries(data).map(([k, v]) => (
//   <div key={k}>
//     <strong>{k}:</strong>{" "}
//     {Array.isArray(v)
//       ? v.map((item, i) => (
//           <div key={i} style={{ marginLeft: "20px" }}>
//             {Object.entries(item).map(([ik, iv]) => (
//               <div key={ik}>
//                 {ik}: {iv}
//               </div>
//             ))}
//           </div>
//         ))
//       : v.toString()}
//   </div>
// ))}