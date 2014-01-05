from pydocx import Docx2Html
from bs4 import BeautifulSoup

def docxtract(file="C:/Users/Gavin/SkyDrive/Documents/Tartarus Falls/sample.docx"):
    valid_keep = ['em', 'i', 'b', 'strong', 'div']
    valid_del = ['hr']
    header = [u'h1', u'h2', u'h3', u'h4']
    html = Docx2Html(file).parsed
    # https://medium.com/p/f2fa442daf99
    html = BeautifulSoup(html, 'html.parser').body
    # clear up the mess
    # http://stackoverflow.com/q/1765848
    for v in valid_keep:
        for match in html.find_all(v):
            match.unwrap()
    for v in valid_del:
        for match in html.find_all(v):
            match.decompose()
    # Get the tree
    p = False
    tree = []
    for child in html.find_all(True):
        if child.name in header:
            if p:
                tree.append([ptext, p])
                p = False
            tree.append(["<b>%s</b>" % child.get_text(), unicode(child)])
        else:
            if child.get_text().strip():
                if p:
                        p = ''.join([p, unicode(child)])
                else:
                    p = unicode(child)
                    ptext = "%s..." % child.get_text()[:80]
    if p:
        tree.append([ptext, p])
    return tree