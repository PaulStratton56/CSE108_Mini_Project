import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

function App() {
  return (
    <div className="App">
      <div className="Container">
        <Login />
      </div>
    </div>
  );
}

function Login(){
    const [showPassword, setShowPassword] = useState(false);

    const toggelPassword = () => {
        setShowPassword(!showPassword);
    }
  return (
    <div>
      <h1 className ="UC-Merced">UC Merced</h1>
        <h2 className = "singleLog "> Single Login</h2>
      <input type="text" placeholder="Username" />
        <input type={showPassword ? "text" : "password"} placeholder="Password" />
        <input type="checkbox" onChange={toggelPassword} /> Show Password
      <button>Login</button>
    </div>
  );
}


export default App;
