mongoose = require 'mongoose'

EventSchema = new mongoose.Schema
  doi: String
  url: String
  story: String
  accessed: Date
  email: String
  location: String
  coords: [ Number, Number ]
  profession: String
  name: String

module.exports = mongoose.model 'Event', EventSchema
