Event = '../models/Event'

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

  # Display a partial entry page
  add: (req, res) ->
    res.render 'Event/add',
      title: 'Add entry'

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    event.save (err, event) ->
      if err
        res.send 500
        console.log err
      else
        res.send status: 'success'
