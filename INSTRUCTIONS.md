## Getting started

### Requirements

 * [Python 2.6 or Python 2.7](http://www.python.org/getit/)
 * [pip](http://www.pip-installer.org/en/latest/installing.html)
 * [mongodb](http://docs.mongodb.org/manual/installation/)
 * [virtualenv](https://pypi.python.org/pypi/virtualenv) (optional but
   recommended)

### Installing

Clone the [git repository](https://github.com/OAButton/server) and set
up:
```
git clone https://github.com/OAButton/server.git /path/to/repo
cd /path/to/repo                     # Switch to the directory where
                                     # you've cloned the repo
git checkout django                  # Switch to the django branch

virtualenv oab-env                   # Set up a new virtualenv (optional)
. oab-env/bin/activate               # Activate the virtualenv (optional)

pip install -r requirements.txt      # Install dependencies

```

### Start mongodb

If the mongodb daemon is not running yet, you can start it locally with
```
mongod --smallfiles -v
```

If you have installed MongoDB via your Debian/Ubuntu package mangager, do
```
sudo service mongodb start
```

### Synchronise the database

This will set up the database ready to use. You only have to do this once:
```
python manage.py syncdb
```
You will be prompted to create a superuser. Reply yes and follow the
instructions.


### Start the webserver

```
python manage.py runserver
```

 * Visit <http://localhost:8000>. Hooray!

### Development

Use of virtualenv is highly recommended for development - it will
ensure that all contributors are using a consistent set of packages.

 * You must be in your virtualenv before you start hacking on oabutton.
 * Remember to activate your virtualenv using (`source env/bin/activate`).
 * Check in settings.py that the line `from settings_local import *`
   is not commented out

#### Virtual machine

If you're familiar with [Vagrant](http://vagrantup.com/) and virtual
machines, there's a Vagrantfile included which will set up and
provision a development VM for you.

### Running the tests

From the directory with the file manage.py in it
```
python manage.py test bookmarklet web
```

### Heroku deployment

 * Ensure that settings.py imports from settings_heroku.py
 * Initial Postgresql Syncing of the database is done with: `heroku run python manage.py syncdb`
   * See: https://devcenter.heroku.com/articles/getting-started-with-django
