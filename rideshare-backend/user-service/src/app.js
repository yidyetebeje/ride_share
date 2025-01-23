require('dotenv').config();  // Load environment variables from .env file

const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const userRoutes = require('./routes/routes');

const app = express();
const initRabbitMQ = async () => {
  try {
      await rabbitmqService.connect();
      
      // Subscribe to driver events
      await rabbitmqService.subscribeToDriverEvents(async (message) => {
          console.log('Received driver event:', message);
          // Handle different driver events here
          switch (message.event) {
              case 'driver.status.updated':
                  // Update user notifications or handle driver status changes
                  break;
              // Add more event handlers as needed
          }
      });
  } catch (error) {
      console.error('Failed to initialize RabbitMQ:', error);
  }
};

initRabbitMQ();

app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB using the MONGO_URI from the environment variables
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('MongoDB connected successfully'))
  .catch(err => console.error('MongoDB connection error:', err));

// Set up routes
app.use('/api/users', userRoutes);


// Start the server using the PORT from the environment variables
const port = process.env.PORT || 3001;  // Default to 3001 if PORT is not set
app.listen(port, () => {
    console.log(`User Service running on http://localhost:${port}`);
});