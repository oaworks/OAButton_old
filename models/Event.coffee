mongoose = require 'mongoose'
$ = require 'jquery'

base_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='

EventSchema = new mongoose.Schema
  name: String
  profession: String
  location: String
  coords: [ Number, Number ]
  accessed: Date
  doi: String
  url: String
  story: String
  email: String

EventSchema.path("location").set (value) ->
  event_schema = this
  $.ajax
    url: base_url + encodeURIComponent(value)
    success: (response) ->
      location = response.results[0].geometry.location
      event_schema.update
        coords: [location.lat, location.lng]
      console.log event_schema
  value

module.exports = mongoose.model 'Event', EventSchema
