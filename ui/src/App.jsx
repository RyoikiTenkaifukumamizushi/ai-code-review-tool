import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MainApp from './MainApp';
import HistoryPage from './HistoryPage';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <nav className="navbar">
          <Link to="/">Home</Link>
          <Link to="/history">History</Link>
        </nav>

        <Routes>
          <Route path="/" element={<MainApp />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
