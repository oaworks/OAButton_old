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
from fabric.api import local, settings, cd, run


def prepare_deploy():
    local("pip install -r requirements.txt")
    local("make test")
    local("git add -p && git commit")
    local("git push")


def deploy():
    code_dir = '/home/ubuntu/dev/OAButton/'
    with settings(warn_only=True):
        with cd(code_dir):
            run("git checkout develop")
            run("git pull")
            run("/home/ubuntu/.virtualenvs/oabutton/bin/pip install -r requirements.txt")
            run("sudo supervisorctl restart oabutton")
