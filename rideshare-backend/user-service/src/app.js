require('dotenv').config();  // Load environment variables from .env file

const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const userRoutes = require('./routes/routes');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB using the MONGO_URI from the environment variables
mongoose.connect('mongodb://127.0.0.1:27017/user-service')
  .then(() => console.log('MongoDB connected successfully'))
  .catch(err => console.error('MongoDB connection error:', err));

// Set up routes
app.use('/api/users', userRoutes);


// Start the server using the PORT from the environment variables
const port = process.env.PORT || 3001;  // Default to 3001 if PORT is not set
app.listen(port, () => {
    console.log(`User Service running on http://localhost:${port}`);
});