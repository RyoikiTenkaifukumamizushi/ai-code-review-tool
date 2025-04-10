import { useRef, useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [file, setFile] = useState(null);
  const [showOutput, setShowOutput] = useState(false);
  const fileInputRef = useRef();
  const [leftWidth, setLeftWidth] = useState(50); // in %

  const handleMouseDown = (e) => {
    const startX = e.clientX;
    const startWidth = leftWidth;

    const handleMouseMove = (e) => {
      const delta = e.clientX - startX;
      const newLeft = Math.min(80, Math.max(20, startWidth + (delta / window.innerWidth) * 100));
      setLeftWidth(newLeft);
    };

    const handleMouseUp = () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  const handleSubmit = async () => {
    if (code.trim() === "" && !file) {
      setFeedback("⚠️ Please enter some code to review.");
      return;
    }

    setLoading(true);
    setFeedback("");
    setShowOutput(true);

    try {
      const formData = new FormData();

      if (file) {
        formData.append("file", file);
      } else {
        formData.append("code", code);
      }

      const response = await fetch("http://localhost:8000/submit/", {
        method: "POST",
        body: formData,
      });

      const result = await response.text();
      setFeedback(result.replace(/\\n/g, '\n')); // fix for escaped \n
    } catch (err) {
      setFeedback("❌ Error during code review.");
      console.error(err);
    }

    setLoading(false);
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const removeFile = () => setFile(null);

  return (
    <div className="app-wrapper">
      <div className="app-header">
        <h1>AI Code Review Tool</h1>
        <p>Paste your code below or upload a file for review</p>
      </div>

      <div className={`editor-area ${showOutput ? 'split' : 'initial-center'}`}>
        <div className="editor-section" style={{ width: showOutput ? `${leftWidth}%` : "90%" }}>
          <div className="textarea-wrapper">
            <CodeMirror
              value={code}
              height="500px"
              extensions={[python()]}
              onChange={(value) => setCode(value)}
              theme="dark"
            />
            <button
              className="file-upload-btn"
              onClick={() => fileInputRef.current.click()}
            >
              <AttachFileIcon fontSize="small" />
            </button>
            <input
              type="file"
              accept=".py"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </div>

          {file && (
            <div className="file-preview">
              <div className="file-info">
                <AttachFileIcon color="primary" />
                <div>
                  <strong>{file.name}</strong>
                  <div className="text-muted">
                    {(file.size / 1024).toFixed(1)} KB
                  </div>
                </div>
                <button className="btn-remove" onClick={removeFile}>Remove</button>
              </div>
            </div>
          )}

          <div className="submit-wrapper">
          <button
          onClick={handleSubmit}
          className="relative inline-flex items-center justify-center px-6 py-3 rounded-full bg-black text-white font-mono tracking-wider shadow-xl transition-transform duration-300 hover:scale-105 focus:outline-none overflow-hidden group"
          >
          {/* Glitchy animated border */}
          <span className="absolute inset-0 rounded-full border-2 border-transparent group-hover:border-blue-400 animate-border-glow"></span>

          {/* Border light trail */}
          <span className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 blur-md opacity-0 group-hover:opacity-70 group-hover:animate-border-light"></span>

          {/* Pulsing AI Core Glow */}
          <span className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-fuchsia-500 opacity-20 group-hover:opacity-30 animate-pulse"></span>

          {/* Foreground content */}
          <span className="relative z-10 flex items-center gap-2 text-sm">
          🤖 Submit for Review
          </span>
          </button>


          </div>
        </div>

        {showOutput && (
          <>
            <div className="resizer" onMouseDown={handleMouseDown} />
            <div className="output-section" style={{ width: `${100 - leftWidth}%` }}>
              <div className="feedback-box">
                {loading ? (
                  <div className="spinner-container">
                    <div className="spinner" />
                    <p>Analyzing your code...</p>
                  </div>
                ) : (
                  <ReactMarkdown>{feedback || "Feedback will appear here."}</ReactMarkdown>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
