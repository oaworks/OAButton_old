Event = require '../models/Event'

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
          res.render 'Event/map',
            title: 'Map view'
            events: events
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
      title: 'Add entry'
      vars:
        url: req.query.url

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    event.save (err, event) ->
      if err then res.send 500, err.message
      else
        res.redirect '/'
