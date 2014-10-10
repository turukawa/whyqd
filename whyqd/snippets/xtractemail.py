import re

def xtractemail(emails):
    """
    Receive a list of emails as a comma-separated value;
    Test against a regex http://www.w3.org/TR/html5/forms.html#valid-e-mail-address and return only the valid ones;
    """
    regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    emails = emails.split(",")
    reg_test = re.compile(regex)
    emails = [e for e in emails if reg_test.match(e)]
    return emails