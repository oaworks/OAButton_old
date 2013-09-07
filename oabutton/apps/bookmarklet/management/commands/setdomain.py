from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (make_option('--domain',
         action='store',
         dest='domain',
         default='oabutton-django.herokuapp.com',
         help='Set the default domain name for the bookmarklet'),)

    def handle(self, *args, **options):
        if options['domain']:
            current_site = Site.objects.get_current()
            current_site.domain = options['domain']
            current_site.save()
            print "Domain set to [%s]" % options['domain']
