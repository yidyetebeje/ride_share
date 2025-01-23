const User = require('../models/models');

class UserService {
    async createUser(userData) {
        const user = new User(userData);
        await user.save();
        return user;
    }

    async getUsers() {
        return User.find().exec();
    }

    async getUserById(userId) {
        return User.findById(userId).exec();
    }
    async requestRide(userId, location) {
        try {
            // Publish ride request event
            await rabbitmqService.publishUserUpdate(userId, 'user.ride.requested', {
                userId,
                location,
                timestamp: new Date().toISOString()
            });
            
            return { message: 'Ride request sent successfully' };
        } catch (error) {
            console.error('Error requesting ride:', error);
            throw error;
        }
    }
}


module.exports = new UserService();