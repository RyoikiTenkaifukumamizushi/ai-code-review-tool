import { useEffect, useState } from "react";
import "./HistoryPage.css";

function HistoryPage() {
  const [entries, setEntries] = useState([]);
  const [openIndex, setOpenIndex] = useState(null); // track which item is open

  useEffect(() => {
    fetch("http://localhost:8000/history/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch history");
        }
        return res.json();
      })
      .then((data) => setEntries(data))
      .catch((err) => console.error("Error fetching history:", err));
  }, []);

  const toggleExpand = (idx) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <div className="history-page">
      <h2>📜 Code Review History</h2>
      <div className="history-scroll-container">
        {entries.length === 0 ? (
          <p>No history found.</p>
        ) : (
          entries.map((item, idx) => (
            <div key={idx} className="history-card">
              <div
                className="history-header"
                onClick={() => toggleExpand(idx)}
              >
                <h4>🕒 {item.timestamp}</h4>
                <span className="toggle-icon">
                  {openIndex === idx ? "▲" : "▼"}
                </span>
              </div>
              {openIndex === idx && (
                <div className="history-details">
                  <h5>🧠 Python Code:</h5>
                  <pre className="code-block">{item.code}</pre>
                  <h5>📝 Review:</h5>
                  <pre className="review-block">{item.review}</pre>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default HistoryPage;
