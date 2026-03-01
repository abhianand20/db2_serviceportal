// import { useEffect, useState } from "react";
// import { apiGet } from "../api/client";
// import { useAppContext } from "../context/AppContext";
// import SummaryCard from "./valueCard";
// import TableCard from "./tableCard";
// import './TableCard.css'


// function DbHealth() {
//   const { server, instance, dbName } = useAppContext();
//   const [data, setData] = useState(null);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     setData(null);
//     apiGet(server, instance, dbName, "/healthcheck")
//     .then((res) => {
//       console.log("API response:", res);
//       setData(res);
//     })
//     .catch((err) => {
//       console.error("API error:", err);
//       setError(err.message);
//     });
  
//   }, [server, instance, dbName]);

//   if (error) return <p style={{ color: "red" }}>Health Error: {error}</p>;
//   if (!data) return <p>Loading DB Health...</p>;

//   return (
//     <div>
//       <h2>DB Health Check</h2>
//       <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>


        
//       {/* <SummaryCard label="DB_START_TIME" value={data.db2_start_time} />
//       <SummaryCard label="DB_Memory Used:" value={data.DB_Memory} />
//       {data.database_connection !== "No Data" ? (   <div className="banner">  Db connection: Failed</div>) :
//     ( <div className="banner"> Db connection: Successful  </div>)}





// {data.last_full_backup == "No Data" ? ( <div className="banner"> No Full backup taken</div>) : (  <TableCard title="Latest Full backup" data={data.last_full_backup}  />)}

// {data.inc_backup_data == "No Data" ?  ( <div className="banner"> No Inc backup taken </div>) :(  <TableCard title="Latest Inc" data={data.inc_backup_data}  />)  }
// {data.log_utilisation !== "No Data" ? (  <TableCard title="Log Utilisation" data={data.log_utilisation}  />) :
//             ( <div className="banner"> Log utilisation Data unavailable </div>)}

     
//       {data.container_status !== "No Data" ? (  <TableCard title="Container Status" data={data.container_status}  />) :
//             ( <div className="banner"> All containers are Good! </div>)}


//       {data.tablespace_issues !== "No Data" ? (  <TableCard title="Container Status" data={data.tablespace_issues}  />) :
//             ( <div className="banner"> All Tablespaces' state is Normal! </div>)}


//       {data.table_issues !== "No Data" ? (  <TableCard title="Container Status" data={data.table_issues}  />) :
//             ( <div className="banner"> All Tables' state is Normal! </div>)}


//        {data.hadr_status !== "No Data" ? (  <TableCard title="Container Status" data={data.hadr_status}  />) :
//             ( <div className="banner"> HADR Not configured</div>)} 

//       {data.loadpending_tables !== "No Data" ? (  <TableCard title="Container Status" data={data.loadpending_tables}  />) :
//             ( <div className="banner"> No tables found in load pending state</div>)} 
             
//              {data.reorgpending_tables !== "No Data" ? (  <TableCard title="Container Status" data={data.reorgpending_tables}  />) :
//             ( <div className="banner"> No tables found in reorg pending state</div>)} 
  

//             {data.indexrebuildpending_tables !== "No Data" ? (  <TableCard title="Container Status" data={data.indexrebuildpending_tables}  />) :
//             ( <div className="banner"> No Index found pending for rebuild</div>)} 
             

//              {data.invalid_views !== "No Data" ? (  <TableCard title="Container Status" data={data.invalid_views}  />) :
//             ( <div className="banner"> No Views invalid</div>)} 
             
//              {data.invalid_packages !== "No Data" ? (  <TableCard title="Container Status" data={data.invalid_packages}  />) :
//             ( <div className="banner"> No invalid package found</div>)} 
             
                          
//              {data.invalid_objects !== "No Data" ? (  <TableCard title="Container Status" data={data.invalid_objects}  />) :
//             ( <div className="banner"> No invalid Objects found</div>)} 
             
                          
//              {data.invalid_triggers !== "No Data" ? (  <TableCard title="Container Status" data={data.invalid_triggers}  />) :
//             ( <div className="banner"> No invalid trigger found</div>)} 
             

                          
//              {data.table_no_pk !== "No Data" ? (  <TableCard title="Container Status" data={data.table_no_pk}  />) :
//             ( <div className="banner"> No tables without primary key found</div>)} 
             


//        </div>*/}

//     </div>
//     </div>
//   );
// }

