import { useState } from 'react'
import './App.css'

function App() {
  const [code , setcode] =useState("");
  const [loading,setLoading]=useState(false);
  const [feedback , setFeedback] = useState("");

  const handlesubmit= () => {
    if(code.trim()===""){
      setFeedback("⚠️ Please enter some code to review.");
    }
  }
  
  return (
    <>
      
    </>
  )
}

export default App
