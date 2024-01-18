// src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatbotResponse, setChatbotResponse] = useState('');

  const handleSubmit = async () => {
    // Send user input to the backend
    const response = await fetch('http://localhost:5000/api/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();
    setChatbotResponse(data.response);
  };

  return (
    <div className="App">
      <h1>Chatbot Interface</h1>
      <div className="chat-container">
        <div className="chat">
          <div className="user-message">{userInput}</div>
          <div className="chatbot-message">{chatbotResponse}</div>
        </div>
      </div>
      <input
        type="text"
        placeholder="Type your message..."
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default App;
