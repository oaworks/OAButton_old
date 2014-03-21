from django.core.urlresolvers import reverse
from oabutton.apps.bookmarklet.models import OABlockedURL
from oabutton.apps.template_email import TemplateEmail
import hashlib
import time


def send_author_notification(author_email, blocked_url):
    """
    Send the author of a paper notification that his paper was
    blocked. Request for an open link.
    """
    md5hash = hashlib.md5(author_email + blocked_url + time.asctime())
    slug = md5hash.hexdigest()
    record = OABlockedURL.objects.create(slug=slug,
                                         author_email=author_email,
                                         blocked_url=blocked_url)
    record.save()

    oa_free_url = reverse('bookmarklet:open_document', kwargs={'slug': slug})

    context = {'blocked_url': blocked_url,
               'oa_free_url': oa_free_url}

    email = TemplateEmail(template='bookmarklet/request_open_version.html',
                          context=context,
                          to=[author_email])
    email.send()
