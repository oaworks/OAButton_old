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
                    'nature.com',
                    'sciencemag.com',
                    'springer.com', ]


def scrape_email(url, domain=None):
    """
    The domain is only required for test cases
    Normally, it's parsed from a network URL
    """
    parsed_url = urlparse.urlparse(url)

    if domain is None:
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
        split_msg = stdoutdata.split('\n')
        status_code = split_msg[0]
        if status_code != 'success':
            # See if 'success' is in the first 10 lines
            if 'success' not in [m.strip() for m in split_msg[:10]]:
                error = split_msg[1:]
                msg = "Networking Error status_code=[%s] error=[%s]" % (status_code, error)
                raise RuntimeError(msg)

        possible_emails = [f[0] for f in re.findall(r'([a-z0-9_\.\-\+]+@[a-z0-9_\-]+(\.[a-z0-9_\-]+)+)', stdoutdata, re.I)]
        if filter_domain:
            possible_emails = [f for f in possible_emails if not f.endswith(domain)]

        possible_emails = set([e.lower() for e in possible_emails])

        # Filter out any emails that have already been sent to this
        # URL
        for email in list(possible_emails):
            from oabutton.apps.bookmarklet.models import OABlockedURL
            block_filter = OABlockedURL.objects.filter(blocked_url=url, author_email=email)
            if block_filter.count():
                possible_emails.remove(email)

        return possible_emails
    return set()
