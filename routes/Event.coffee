Event = require '../models/Event'

module.exports =

  # Display a list of story
  index: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.render 'Event/list',
          events: events

  # Display data as JSON
  index_json: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.json events

  # Display an entry page
  add: (req, res) ->
    res.render 'Event/add_iframe',
      title: 'Add entry'

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    event.save (err, event) ->
      if err then res.send 500, err.message
      else
        res.redirect '/'
