## Getting started

### Requirements

 * Python 2.6 or Python 2.7 ([install](http://www.python.org/getit/))
 * virtualenv ([install](https://pypi.python.org/pypi/virtualenv))
 * pip ([install](http://www.pip-installer.org/en/latest/installing.html))

### Installing

```
git clone https://github.com/OAButton/server.git /path/to/repo  # clone [the project code](https://github.com/OAButton/server)
cd /path/to/repo  # Switch to the directory where you've cloned the repo
git checkout django  # Switch to the django branch

virtualenv ENV  # Set up a new virtualenv
source env/bin/activate  # Start the virtualenv

pip install -r requirements/dev.txt  # Install the dependencies

cd oabutton  # Switch to the django home directory
python manage.py syncdb  # sync the database
```


### Start mongodb

If the mongodb daemon is not running yet, you can start it locally
with :
```
mongod --smallfiles -v
```


### Start the webserver

```
python manage.py runserver
```

 * visit <http://localhost:8000>. Hooray!

### Development

 * You must be in your virtualenv before you start hacking on oabutton.  
 * You can start your virtualenv using (`source env/bin/activate`).
 * settings.py must be import from settings_local.py

### Heroku deployment

 * Ensure that settings.py imports from settings_heroku.py
 * Initial Postgresql Syncing of the database is done with: `heroku run python manage.py syncdb`
   * See: https://devcenter.heroku.com/articles/getting-started-with-django


### Running the tests

From the directory with the file manage.py in it :
```
python manage.py test bookmarklet web
```
