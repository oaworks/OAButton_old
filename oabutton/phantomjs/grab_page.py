import subprocess
import re
import tempfile


js_template = r"""
var page = require('webpage').create();
var url = "%URL%";
page.settings.resourceTimeout = 5000; // 5 seconds
page.onResourceTimeout = function(e) {
    console.log(e.errorCode);   // it'll probably be 408
    console.log(e.errorString); // it'll probably be 'Network timeout on resource'
    console.log(e.url);         // the url whose request timed out
    phantom.exit(1);
};

page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36';
page.open(url, function (status) {
    page.evaluate(function () {
        return document.title;
    }, function(result){

    });
    console.log(page.content);
    phantom.exit();
});
"""


def grab_emails(url):
    script = js_template.replace("%URL%", url)
    with tempfile.NamedTemporaryFile(suffix='.js', delete=True) as tmpfile:
        tmpfile.write(script)
        tmpfile.flush()
        command = 'phantomjs %s' % tmpfile.name
        child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = child.communicate()
        possible_emails = set([f[0] for f in re.findall(r"(\w+@\w+(\.\w+))", stdoutdata)])
        return possible_emails
    return set()
