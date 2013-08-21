import scraperwiki
import requests
import lxml.html
from lxml.html import tostring
import re

def unescape(text):
    import re, htmlentitydefs
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fixup, text)

def absolute_urls(text, baseurl):
    return re.sub('(href|src)="(?!https?://)([^"]+)"', '\g<1>="' + baseurl + '\g<2>"', text)

html = requests.get(baseurl)
dom = lxml.html.fromstring(html.text)

baseurl = 'http://datajournalismhandbook.org/1.0/en/'
i = j = 1

for a in dom.cssselect('#main h2 a'):
    section = {
        'title': a.text,
        'url': baseurl + a.get('href'),
        'section_number': i
    }
    scraperwiki.sqlite.save(['title','url'], section, 'sections')

    for a2 in a.getparent().getnext().cssselect('a'):
        chapter = {
            'title': a2.text,
            'url': baseurl + a2.get('href'),
            'chapter_number': j,
            'section_number': i
        }
        html2 = requests.get(chapter['url'])
        dom2 = lxml.html.fromstring(html2.text)
        chapter['html'] = absolute_urls(unescape(tostring(dom2.cssselect('div.sect2')[0])), baseurl)
        scraperwiki.sqlite.save(['title','url'], chapter, 'chapters')
        j = j + 1

    i = i + 1
