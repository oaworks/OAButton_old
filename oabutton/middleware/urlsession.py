from django.conf import settings as s


class FakeSessionCookieMiddleware(object):
    """
    This is totally unsafe to use outside of an SSL enviroment.
    """
    def process_request(self, req):
        if not s.SESSION_COOKIE_NAME in req.COOKIES \
                and s.SESSION_COOKIE_NAME in req.GET:
            req.COOKIES[s.SESSION_COOKIE_NAME] = \
                req.GET[s.SESSION_COOKIE_NAME]
