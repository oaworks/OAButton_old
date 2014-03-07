import subprocess
import re
import tempfile


def grab_emails(url):
    data = open('loadit_template.js', 'r').read()
    script = data.replace("%URL%", "http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100?view=abstract")
    with tempfile.NamedTemporaryFile(suffix='.js', delete=True) as tmpfile:
        tmpfile.write(script)
        tmpfile.flush()
        command = 'phantomjs %s' % tmpfile.name
        child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = child.communicate()
        possible_emails = set([f[0] for f in re.findall(r"(\w+@\w+(\.\w+))", stdoutdata)])
        return possible_emails
    return set()


print "Found emails: ", grab_emails("http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100?view=abstract")
