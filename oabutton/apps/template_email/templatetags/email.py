from django.template import Library, Node


register = Library()


def do_email_tag(parser, token):
    tag = token.contents
    nodelist = parser.parse(('end%s' % tag,))
    parser.delete_first_token()
    return EmailNode(tag, nodelist)


class EmailNode(Node):
    def __init__(self, tag, nodelist):
        self.tag = tag
        self.nodelist = nodelist

    def render(self, context):
        context_var = '_%s' % self.tag
        if not context.get(context_var, False):
            return ''
        return self.nodelist.render(context)


register.tag('subject', do_email_tag)
register.tag('body', do_email_tag)
register.tag('bodyhtml', do_email_tag)
