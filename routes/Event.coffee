Event = require '../models/Event'
http  = require 'http'

module.exports =

  # Display a list of story
  show_stories: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.render 'Event/list',
          title: 'Stories'
          events: events

  show_map: (req, res) ->
    Event.find({}).exec (err, events) ->
      Event.find({}).count (err, count) ->
        if err then res.send 500
        else
          coords = (event.coords for event in events)
          res.render 'Event/map',
            title: 'Map'
            events: JSON.stringify events
            count: count

  # Display data as JSON
  get_json: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.json events

  # Display an entry page
  add: (req, res) ->
    res.render 'Event/add_iframe',
      vars:
        url: req.query.url

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    coords = req.body['coords'].split ','
    event.coords.lat = coords[0]
    event.coords.lng = coords[1]
    event.save (err, event) ->
      if err then res.send 500, err.message
      else
        res.render 'Event/success'
