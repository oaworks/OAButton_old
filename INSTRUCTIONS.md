## Getting started

### Requirements

 * [Python 2.6 or Python 2.7](http://www.python.org/getit/)
 * [pip](http://www.pip-installer.org/en/latest/installing.html)
 * [mongodb](http://docs.mongodb.org/manual/installation/)
 * [virtualenv](https://pypi.python.org/pypi/virtualenv) (optional but
   recommended)
 * [PhantomJS](http://phantomjs.org/) (required to run automated
   Javascript tests)
 * [PhantomJS] is now required to dump email addresses from remote
   servers

### Installing

Clone the [git repository][repo] and set up:
```
git clone https://github.com/OAButton/OAButton.git /path/to/repo
cd /path/to/repo                     # Switch to the directory where
                                     # you've cloned the repo
git checkout develop                  # Switch to the develop branch

virtualenv oab-env                   # Set up a new virtualenv (optional)
. oab-env/bin/activate               # Activate the virtualenv (optional)

pip install -r requirements.txt      # Install dependencies

flake8 --install-hook                # Install the flake8 pre-commit hook
                                     # Checks your code for PEP8 compliance
```

### Set up your local environment

Save a copy of `oabutton/settings_local.py.example` without the .example suffix
in the same folder, and change the DB_USER to the username under which the
application will start. 

If you don't have a CORE API key, the app will still run, but you'll get
warnings and communications with [CORE](http://core.kmi.open.ac.uk/)
will fail.  An API key is not required to run the tests, as the API
accesses are mocked out.

### Start mongodb

If the mongodb daemon is not running yet, you can start it locally with
```
mongod --smallfiles -v
```

If you have installed MongoDB via your Debian/Ubuntu package mangager, do
```
sudo service mongodb start
```

### Create the postgres role and database
```
sudo su - postgres
createuser -s -r <username>
psql -c 'create database oabutton;' -U <username>
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

We are using LESSC to compile stylesheets from LESS to CSS. The compiler is
run from a Makefile. Install Node.js then `npm install lessc -g`, then run
`make` from the root folder to update CSS.

### Running the tests

From the directory with the file manage.py in it, run the Python tests
with:
```
python manage.py test bookmarklet web
```

Run the JavaScript tests with:
```
phantomjs scripts/qunit-runner.js oabutton/static/test/test.html
```

If you have `make` installed, you can also just run:
```
make test
```

### Heroku deployment

 * Ensure that settings.py imports from settings_heroku.py
 * Initial Postgresql Syncing of the database is done with: `heroku run python manage.py syncdb`
   * See: https://devcenter.heroku.com/articles/getting-started-with-django

Required enviroment variables

## Getting started with a virtual machine

If you're familiar with [Vagrant](http://vagrantup.com/) and virtual
machines, there's a Vagrantfile included which will set up and
provision a development VM for you.

If you're not familiar, here's a lightning tutorial. After installing
VirtualBox and Vagrant, and cloning the [git repository][repo]:

1. Open a command line and change to the directory where you cloned
   the repository
2. Start up the virtual machine: `vagrant up`
    * This will take a while the first time you do it, while it
      downloads the machine image and installs various prerequisites.
3. Log into the virtual machine via SSH: `vagrant ssh`
    * You should now have a commandline open in your virtual machine.
4. Change to the vagrant shared directory: `cd /vagrant`
    * The repository you cloned will automatically be mounted at
      `/vagrant`, so you can edit the files there using your favourite
      text editor *outside the VM* and all changes will be visible
      inside the VM as well.  Just restart the server when you need
      to.
5. Activate the virtualenv environment: `source env/bin/activate`
6. Start the development server: `python manage.py runserver
   192.168.33.10:8000`
    * Note the IP address on the end: if you omit this, 
7. Point your web browser to <http://192.168.33.10:8000>

When you've finished working, you can quit the webserver if it's still
running (`CTRL-C`), log out of the virtual machine (`exit`) and then
either:

* Shut down the VM: `vagrant halt`
* Suspend the VM to disk: `vagrant suspend`

Then next time you're ready to work, follow the instructions above
again: step 2 will take much less time as the VM is already installed
and configured and just needs to boot.

If you ever need to completely reset the VM, just delete it with
`vagrant destroy` and start again.

[repo]: http://github.com/OAButton/OAButton
