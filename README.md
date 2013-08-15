## Open Access Button

A prototype version of the Open Access Button idea explained in [this blog](http://oabutton.wordpress.com/2013/07/06/our-project-short-version/).

This is the Python port.

Dev Requirements:

* Python 2.6 or Python 2.7
* virtualenv
* virtualenvwrapper

OSX instructions:

The easiest way to get everything working is to use Homebrew 

TODO: add link to homebrew

TODO: double check the following instructins
$ brew install python
$ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
$ tar xvfz virtualenv-X.X.tar.gz
$ cd virtualenv-X.X
$ python setup.py install
$ pip install virtualenvwrapper

Now change to the parent directory of where your oabutton source should go. I do everything under ~/dev.

$ cd ~/dev
$ git clone git@github.com:OAButton/server.git

Switch to the Django branch
$ git checkout django
$ make

TODO: add instructions for installing MongoDB and how to verify that
Mongo is running properly.

TODO: we should probably setup docker images for this stuff so that
it's easy to deploy.

That should be it.  Go to http://localhost:8000/ and have at it.

Go to http://localhost:8000 on your browser and you're done.

Licensed under the MIT license.
