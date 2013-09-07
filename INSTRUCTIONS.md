## Getting started

### Installing

 * [Clone the repo](https://github.com/OAButton/server) (the project code)
 * [Install node.js](http://nodejs.org/) (the framework). If you use brew, `brew install node` does the trick!
 * [Install mongo db](http://www.mongodb.org/downloads) (the database engine). If you use brew, `brew install mongodb` works for us!
 * Go to the directory where you’ve cloned the repo (`/path/to/server`)
 * type `npm install` to install the dependencies

### Running the server

 * if it’s not already running, start mongo with `mongod`
 * then in a new tab, start the webserver with `node web.js`
 * visit <http://localhost:3000>. Hooray!

### Additional Ubuntu 13.04 notes

Replace steps 2 and 3 in the above with:

 * [Add and install the required node.js version] sudo add-apt-repository ppa:chris-lea/node.js
 * [Install the prerequisites] sudo apt-get update && sudo apt-get install mongodb nodejs
