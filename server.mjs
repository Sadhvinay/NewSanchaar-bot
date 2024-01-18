// server.mjs
import express from 'express';
import bodyParser from 'body-parser';
import { PythonShell } from 'python-shell';

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json()); // Use express.json() instead of json()

app.post('/api/chatbot', (req, res) => {
  const userMessage = req.body.message;

  // Run the Python script with user input
  const options = {
    scriptPath: './',  // Adjust this path based on your project structure
    args: [userMessage],
  };

  PythonShell.run('chatbot.py', options, (err, results) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      const chatbotResponse = results[0];
      res.json({ response: chatbotResponse });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
