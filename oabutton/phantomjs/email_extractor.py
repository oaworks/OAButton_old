import subprocess
import re
import tempfile
import urlparse


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
    console.log(status);
    console.log(page.content);
    phantom.exit();
});
"""

# This list of domains will be filtered out when checking for author
# email addresses
DOMAIN_BLACKLIST = ['elsevier.com',
                    'sciencemag.com',
                    'springer.com', ]


def scrape_email(url):
    parsed_url = urlparse.urlparse(url)
    domain = parsed_url.netloc.replace("www.", '')

    filter_domain = domain in DOMAIN_BLACKLIST

    script = js_template.replace("%URL%", url)
    with tempfile.NamedTemporaryFile(suffix='.js', delete=True) as tmpfile:
        tmpfile.write(script)
        tmpfile.flush()
        command = 'phantomjs %s' % tmpfile.name
        child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = child.communicate()

        # PhantomJS sticks in an error statuscode at the top for
        # anything other than 200 success
        split_msg = stdoutdata.split()
        status_code = split_msg[0]
        if status_code != 'success':
            error = split_msg[1:]
            raise RuntimeError("Networking Error", status_code=status_code, error=error)

        if filter_domain:
            possible_emails = set([f[0] for f in re.findall(r'([a-z0-9_\-]+@[a-z0-9_\-]+(\.[a-z0-9_\-]+))', stdoutdata) if not f[0].endswith(domain)])
        else:
            possible_emails = set([f[0] for f in re.findall(r'([a-z0-9_\-]+@[a-z0-9_\-]+(\.[a-z0-9_\-]+))', stdoutdata)])
        return possible_emails
    return set()
