"""
The easy button for deployment

Add your SSH key :

    $ ssh-add ~/.ssh/oabutton.pem
    Identity added: /Users/victorng/.ssh/oabutton.pem (/Users/victorng/.ssh/oabutton.pem)

# Run prepare_deploy:

    $ fab prepare_deploy

# Run deploy:

    $ fab -H ubuntu@staging.openaccessbutton.org deploy

"""
from fabric.api import local, settings, cd, run, env
from os.path import join


def prepare_deploy():
    local("pip install -r requirements.txt")
    local("make test")
    local("git add -p && git commit")
    local("git push")


def deploy():
    code_dir = '/home/ubuntu/dev/OAButton/'
    BIN_DIR = "/home/ubuntu/.virtualenvs/oabutton/bin"
    PIP_BIN = join(BIN_DIR, 'pip')
    PYTHON_BIN = join(BIN_DIR, 'python')
    with settings(warn_only=True):
        with cd(code_dir):
            run("git pull")
            run("git checkout %s" % env.release_tag)
            run("%s install -r requirements.txt" % PIP_BIN)
            version_path = join(code_dir,
                                'oabutton',
                                'static',
                                'public',
                                'version.txt')
            run("git rev-parse --short HEAD > %s" % version_path)
            # We don't need syncdb anymore as south is enabled now
            #run("%s manage.py syncdb" % PYTHON_BIN)
            run("%s manage.py migrate bookmarklet" % PYTHON_BIN)
            run("sudo supervisorctl restart oabutton")
