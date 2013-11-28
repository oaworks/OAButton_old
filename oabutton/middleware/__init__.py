from django.conf import settings as s

import re

CSS_HREF = re.compile("(href=\"/static/css[^\"].*)\"")
JS_HREF = re.compile("(src=\"/static/js[^\"]*)\"")


class StaticCacheBuster(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        result = view_func(request, *view_args, **view_kwargs)
        if "Content-Type: text/html" in result.serialize_headers():
            result.content = CSS_HREF.sub("\\1?version=%s\"" % s.VERSION, result.content)
            result.content = JS_HREF.sub("\\1?version=%s\"" % s.VERSION, result.content)
        return result
