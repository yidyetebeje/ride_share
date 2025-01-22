const express = require('express');
const userController = require('../controllers/controller');

const router = express.Router();

router.post('/', userController.registerUser);
router.get('/', userController.listUsers);
router.get('/:id', userController.getUser);

module.exports = router;