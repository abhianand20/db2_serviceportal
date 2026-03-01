import TableCard from "./tableCard"
import SummaryCard from "./valueCard"
import { useState } from "react";



function Card({Title,isActive,onToggle}){

return(
    <div
    onClick={onToggle}
    style={{
      minWidth: "160px",
      maxWidth: "180px",
      height:"160px",
      padding: "10px",
      borderRadius: "12px",
      backgroundColor: isActive? "#e5de12" :"#8be0f3",
      boxShadow: "0 4px 6px rgba(30, 144, 60, 0.08)",
      textAlign: "center",
      display: "flex",
      flexDirection: "column",
      gap: "15px",
      boxSizing:"border-box"
    }}
  >
    <h3 style={{ margin: 0 }}>{Title}</h3>

    <button
     
      style={{
        padding: "6px 12px",
        cursor: "pointer",
        color:" "

      }}
    >
      {isActive ? "Hide Data" : "Show Data"}
    </button>
  </div>
);
}

function DetailedSec({Title,data=[],Message, isActive}){
    const isArray = Array.isArray(data) && data.length > 0;
    const isValue = !Array.isArray(data) && data !== "No Data" && data !== null && data !== undefined;
  
return(
<>
    <div
      style={{
        flex: "0 0 auto",
        width: isArray? "100%":"100px",
        minWidth: isArray? "100%":"130px",
        maxWidth: "150px",
        marginTop: "12px",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        boxSizing:"border-box",
        background: isActive ? "#black" : "#f0f8ff",
        padding: isActive? "10px" : "0px",
        borderRadius: isActive? "8px" : "0px",
        boxShadow: isActive? "0 4px 6px rgba(30, 144, 60, 0.1)" : "none"

      }}
    >
      { isArray ? (
        <TableCard title={Title} data={data} />
      ) : isValue ? (
        <SummaryCard label={Title} value={data} isActive={isActive}  />
      ) : (
        <div className="summary-card">{Message}</div>
      )}
    </div>
</>
);

}




export { Card, DetailedSec };

