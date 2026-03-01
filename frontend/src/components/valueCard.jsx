// src/components/SummaryCard.jsx
import './valueCard.css';

function SummaryCard({ label, value }) {
  return (
    <div className="summary-card"
    // style={
    //   isActive
    //   ? {
    //       background: "#e5de12",
    //       padding: "10px",
    //       borderRadius: "8px",
    //       boxShadow: "0 4px 6px rgba(100, 218, 10, 0.1)",
    //     }
    //   : { background: "#e5de12",
    //     padding: "10px",
    //     borderRadius: "8px",
    //     boxShadow: "0 4px 6px rgba(100, 218, 10, 0.1)",}
    // }
    
    >
      <div className="summary-label">{label}</div>
      <div className="summary-value">{String(value)}</div>
    </div>
  );
}

export default SummaryCard;
