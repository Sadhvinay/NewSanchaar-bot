import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatbotResponse, setChatbotResponse] = useState('');
  const apiUrl = 'http://localhost:5000/api/chatbot';

  const handleSubmit = async () => {
    try {
      // Send user input to the backend
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setChatbotResponse(data.response);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Handle error gracefully, e.g., display an error message to the user
    }
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
