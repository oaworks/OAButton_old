from oabutton.apps.bookmarklet.models import *

emails = set([(x.name, x.email) for x in OAUser.objects.all() if x.mailinglist])
f = open('/tmp/foo.txt','w')
for x in emails:
    f.write("%s <%s>\r\n" % (x[0].encode('utf8'), x[1].encode('utf8')))
