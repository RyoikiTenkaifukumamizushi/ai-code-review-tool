import { useState, useRef } from 'react';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import './App.css';

function App() {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [file, setFile] = useState(null);
  const fileInputRef = useRef();

  const handleSubmit = () => {
    if (code.trim() === "" && !file) {
      setFeedback("⚠️ Please enter some code to review.");
      return;
    }

    setLoading(true);
    setFeedback("");

    setTimeout(() => {
      setLoading(false);
      setFeedback("✅ Good use of a function! Consider adding type hints for better clarity.");
    }, 2000);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) setFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) setFile(droppedFile);
  };

  const handleDragOver = (e) => e.preventDefault();
  const removeFile = () => setFile(null);

  return (
    <div className="app-wrapper">
      <div className="app-header">
        <h1>AI Code Review Tool</h1>
        <p>Paste your code below or upload a file for review</p>
      </div>

      <div className="editor-container">
        <div className="textarea-wrapper">
          <textarea
            className="nice-textarea"
            placeholder="Paste your code here or drop a file..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            rows={8}
          />
          <button
            className="file-upload-btn"
            onClick={() => fileInputRef.current.click()}
          >
            <AttachFileIcon fontSize="small" />
          </button>
          <input
            type="file"
            accept=".txt,.py,.js,.java,.cpp"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: "none" }}
          />
        </div>

        {/* File preview (optional) */}
        {file && (
          <div className="file-preview">
            <div className="d-flex align-items-center gap-2">
              <AttachFileIcon color="primary" />
              <div>
                <strong>{file.name}</strong>
                <div className="text-muted" style={{ fontSize: "0.9em" }}>
                  {(file.size / 1024).toFixed(1)} KB
                </div>
              </div>
              <button className="btn btn-sm btn-outline-danger ms-auto" onClick={removeFile}>
                Remove
              </button>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button onClick={handleSubmit} className="btn-gradient">
          🚀 Submit for Review
        </button>

        {/* Feedback or warning BELOW the button */}
        <div className="feedback-box">
          {loading ? "🔄 Reviewing your code, please wait..." : feedback || "Feedback will appear here."}
        </div>
      </div>
    </div>
  );
}

export default App;
