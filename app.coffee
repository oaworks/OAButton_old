express  = require 'express'
flash    = require 'connect-flash'
manifest = require './package.json'
minify   = require 'express-minify'
mongoose = require 'mongoose'
path     = require 'path'
Event    = require './models/Event'
Event_route = require './routes/Event'


APP_HOST_ADDRESS     = process.env.HOST || "0.0.0.0"
APP_PORT_NUMBER      = process.env.PORT || 3000
APP_DOMAIN           = process.env.HOST || APP_HOST_ADDRESS + ":" + APP_PORT_NUMBER
APP_MONGODB_URL      = process.env.MONGOLAB_URI || 'mongodb://'+APP_HOST_ADDRESS+'/'+manifest.name+'-dev'

app = module.exports = express()


## Configuration

app.configure ->
  app.set 'port', APP_PORT_NUMBER
  app.set 'views', __dirname + '/views'
  app.set 'view engine', 'jade'
  app.use express.logger()
  app.use express.bodyParser()
  app.use express.cookieParser()
  app.use express.methodOverride()
  app.use express.session
    secret: 'bmjhack'
  app.use flash()
  app.use minify()
  app.use app.router
  app.use express.static path.join(__dirname, "public")
  app.set 'connstr', APP_MONGODB_URL

app.configure 'development', ->
  app.use express.errorHandler
    dumpExceptions: true
    showStack: true
  app.locals.pretty = true

app.configure 'production', ->
  app.use express.errorHandler
    dumpExceptions: false
    showStack: false

## MongoDB

db = mongoose.connection
db.on 'error', (console.error.bind console, 'connection error: ')
db.on 'open', -> console.log 'Connected to '+(app.get 'connstr')
mongoose.connect app.get 'connstr'

console.log 'Connecting to: '+(app.get 'connstr')

app.get '/', (req, res) ->
  add_calendar_date = (event) ->
    event.calendar_date = event.accessed.calendar()
    return event
  Event.find({}).exec (err, events) ->
    if err then res.send 500
    else
      res.render 'index.jade',
        events: JSON.stringify (add_calendar_date event for event in events)
        count: events.length
        domain: APP_DOMAIN

# Display data as JSON
app.get '/api', (req, res) ->
  Event.find({}).exec (err, events) ->
    if err then res.send 500
    else
      res.json events

app.get '/stories',       Event_route.show_stories

# These are hidden from main page for bookmarklet
app.get  '/add', Event_route.add
app.post '/add', Event_route.add_post

## Run the server

app.listen (app.get 'port'), -> console.log 'Listening on :' + app.get 'port'
