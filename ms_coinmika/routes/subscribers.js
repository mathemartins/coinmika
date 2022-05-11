const express = require('express');
const router = express.Router();
const Subscriber = require('../models/subscriber')


// Get all subscribers
router.get('/', async (req, res) => {
    try {
        const subscribers = await Subscriber.find()
        res.json(subscribers)
    } catch (err) {
        res.status(500).json({"message":err.message});
    }
});


// Getting One
router.get('/:id', getSubscriber, (req, res) => {
    res.json(res.subscriber)
})


async function getSubscriber(req, res, next) {
    let subscriber
    try {
        subscriber = await Subscriber.findById(req.params.id)
        if (subscriber == null) {
        return res.status(404).json({ message: 'Cannot find subscriber' })
        }
    } catch (err) {
        return res.status(500).json({ message: err.message })
    }

    res.subscriber = subscriber
    next()
}

module.exports = router