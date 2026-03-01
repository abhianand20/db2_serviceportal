import './tableCard.css'
function TableCard( {title, data=[]}){

    
    const columns = data.length > 0 ? Object.keys(data[0]) : [];
    console.log(data)
    if (!columns.length) return <p>No data available</p>;

return(

    <div className="table-card">
    <h3> {title}</h3>

   <div className="table-wrapper">
    <table>
    <thead>       
    <tr>
        { columns.map(col =>(
            <th key={col}>{col} </th>
        ))}
     </tr>
    </thead>   

    <tbody>
        {data.map((row,rowindex) =>(
            <tr key={rowindex}>
                {Object.entries(row).map(([key,value]) => (
                 <td key={key} className={String(value).length > 50 ? "sql-cell" : ""}
                 title={String(value)}  > {value}</td>
                ))}
                </tr>

        ))}
    </tbody>
    </table>
   </div>
   </div>

)}

export default TableCard