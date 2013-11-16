import fabric
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
            run("git pull")
            run("sudo supervisorctl restart oabutton")
