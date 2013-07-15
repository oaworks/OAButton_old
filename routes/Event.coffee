Event = require '../models/Event'
http  = require 'http'

module.exports =

  # Display a list of stories
  show_stories: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.render 'stories',
          title: 'Stories'
          events: events
          count: events.length

  show_map: (req, res) ->
    add_calendar_date = (event) ->
      event.calendar_date = event.accessed.calendar()
      return event
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.render 'map',
          title: 'Map'
          events: JSON.stringify (add_calendar_date event for event in events)
          count: events.length

  # Display data as JSON
  get_json: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.json events

  # Display an entry page
  add: (req, res) ->
    res.render 'sidebar/index',
      vars:
        url: req.query.url
        doi: req.query.doi

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    coords = req.body['coords'].split ','
    event.coords.lat = coords[0]
    event.coords.lng = coords[1]
    event.save (err, event) ->
      if err then res.send 500, err.message
      else
        scholar_url = ''
        if req.body['doi']
          scholar_url = 'http://scholar.google.com/scholar?cluster=' + encodeURIComponent('http://dx.doi.org/' + req.body['doi'])
        res.render 'sidebar/success',
          scholar_url: scholar_url

