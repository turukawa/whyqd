from bs4 import BeautifulSoup

def mergediff(html, valid_tags = ['b', 'i', 'u', 'strong', 'em', 'blockquote']):
    # http://stackoverflow.com/q/1765848
    soup = BeautifulSoup(html)
    for match in soup.findAll('ins'):
        match.replaceWithChildren()
    for match in soup.findAll('del'):
        match.decompose()
    # http://tezro.livejournal.com/219164.html
    empty_tags = soup.findAll(lambda tag: tag.name in valid_tags and not tag.contents and (tag.string is None or not tag.string.strip()))
    [empty_tag.extract() for empty_tag in empty_tags]
    return unicode(soup)