mongoose = require 'mongoose'

EventSchema = new mongoose.Schema
  name: String
  profession: String
  location: String
  coords:
    lat: Number
    lng: Number
  accessed: Date
  doi: String
  url: String
  story: String
  email: String

module.exports = mongoose.model 'Event', EventSchema
