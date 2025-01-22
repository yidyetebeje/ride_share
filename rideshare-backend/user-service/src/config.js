require('dotenv').config();

module.exports = {
    mongoURI: process.env.MONGO_URI || 'mongodb://user-db:27017/user_service',
    port: process.env.PORT || 3001,
};