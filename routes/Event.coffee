Evt = '../models/Event'

module.exports =

  # Display a list of story
  index: (req, res) ->
    Event
      .find {}
      .exec (err, events) ->
        if err
          res.send 500
          console.log err
        else
          res.render 'Event/list',
            events: events

  # Display an entry page
  add: (req, res) ->
    res.render 'Event/add_iframe',
      title: 'Add entry'

  # Handle POST
  add_post: (req, res) ->
    evt = new Evt req.body
    evt.save (err, evt) ->
      if err then res.send 500, err.message
      else
        res.redirect '/'
