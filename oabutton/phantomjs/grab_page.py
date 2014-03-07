import subprocess
import re

command = r"""phantomjs loadit.example.js"""
child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdoutdata, stderrdata = child.communicate()
possible_emails = set([f[0] for f in re.findall(r"(\w+@\w+(.\w+))", stdoutdata)])
print "Found emails: ", possible_emails
