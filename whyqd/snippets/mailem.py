from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(*args, **kwargs):
    """
    Send email handler; kwargs to include:
        to (email, or in form '<First Last> email@domain.com')
        subject (string)
        template (string)
        context (dict with appropriate refs for template)
        sendhtml (boolean, optional)
    """
    email = Emailer(to=kwargs.get('to'), subject=kwargs.get('subject'))
    email.text('{0}/mail/{1}.txt'.format(
        settings.TEMPLATE_DIRS[0], kwargs.get('template')), kwargs.get('context'))
    if kwargs.get('sendhtml', False):
        email.html('{0}/mail/{1}.html'.format(
            settings.TEMPLATE_DIRS[0], kwargs.get('template')), kwargs.get('context'))
    email.send()

class Emailer():
    """
    A wrapper around Django's EmailMultiAlternatives
    that renders txt and html templates.
    Example Usage:
    >>> email = Emailer(to='oz@example.com', subject='A great non-spammy email!')
    >>> ctx = {'username': 'Oz Katz'}
    >>> email.text('templates/email.txt', ctx)
    >>> email.html('templates/email.html', ctx)  # Optional
    >>> email.send()
    >>>
    Reference: https://gist.github.com/ozkatz/5520308
    """
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
    
    def _render(self, template, context):
        return render_to_string(template, context)
 
    def html(self, template, context):
        self._html = self._render(template, context)
 
    def text(self, template, context):
        self._text = self._render(template, context)
 
    def send(self, from_addr=None, fail_silently=False):
        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = getattr(settings, 'EMAIL_FROM_ADDR')
        msg = EmailMultiAlternatives(
            self.subject,
            self._text,
            from_addr,
            self.to
        )
        if self._html:
            msg.attach_alternative(self._html, 'text/html')
        msg.send(fail_silently)