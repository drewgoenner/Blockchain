import React, {useState, useEffect} from 'react';
import Wallet from './components/Wallet'

const baseURL = 'http://localhost:5000';

function App() {
  

  return (
    <div className="App">
     
    <Wallet />
    </div>
  );
}

export default App;
