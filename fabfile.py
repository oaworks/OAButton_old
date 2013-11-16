import fabric
from fabric.api import local

def prepare_deploy():
    local("pip install -r requirements.txt")
    local("make test")
    local("git add -p && git commit")
    local("git push")
