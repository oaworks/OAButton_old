from oabutton.apps.bookmarklet.models import OAEvent, OAUser
from django.db import transaction
import dateutil.parser
import json

def go():
    print "Migrating Users"
    with open('/tmp/users.json', 'r') as user_file:
        for i, line in enumerate(user_file):
            print "Migrating user %d" % i
            try:
                jdata = json.loads(line)
                with transaction.autocommit():
                    user = OAUser.objects.create(name=jdata['name'],
                            email=jdata['email'],
                            profession=jdata['profession'],
                            mailinglist=jdata['mailinglist'],
                            slug=jdata['_id'],)
                    user.save()
            except Exception, e:
                print "Can't migrate user.  Data: [%s] error: %s" % (jdata, e)
                transaction.rollback()

    with open('/tmp/events.json', 'r') as event_file:
        for i, line in enumerate(event_file):
            print "Migrating event %d" % i
            try:
                jdata = json.loads(line)
                with transaction.autocommit():
                    evt = OAEvent.objects.create(location=jdata['location'],
                            coords=jdata['coords'],
                            accessed=dateutil.parser.parse(jdata['accessed']),
                            doi=jdata['doi'],
                            url=jdata['url'],
                            story=jdata.get('story', ''),
                            description=jdata.get('description', ''),
                            user_slug=jdata['user_id'],
                            user_email='',
                            user_name=jdata['user_name'],
                            user_profession=jdata['user_profession'],)
                    evt.save()
            except Exception, e:
                print "Can't migrate event.  Data: [%s] error: %s" % (jdata, e)
                transaction.rollback()
