mongoose = require 'mongoose'
moment   = require 'moment'

moment.lang 'en-gb'

EventSchema = new mongoose.Schema
  name: String
  profession: String
  location: String
  coords:
    lat: Number
    lng: Number
  accessed:
    type: Date
    get: (dt) -> moment dt
  calendar_date: String
  doi: String
  url: String
  story: String
  email: String

module.exports = mongoose.model 'Event', EventSchema
