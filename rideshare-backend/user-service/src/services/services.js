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
}

module.exports = new UserService();