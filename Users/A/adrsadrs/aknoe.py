import scraperwiki, re, time
import lxml.html
from lxml.html.clean import clean_html
from BeautifulSoup import BeautifulSoup

###
def shorten(url):
    from urllib2 import urlopen, Request, HTTPError
    from urllib import quote
    from simplejson import loads
    try:
        e = urlopen(Request('http://goo.gl/api/url','url=%s'%quote(url),{'User-Agent':'toolbar'}))
        j = loads(e.read())
        return j['short_url']
    except:
        return(url)

### 

def get_eintrag_links():
    url = "http://extranet.aknoe.at/haendeweg.nsf/INETF!OpenForm&Start=1&Count=10000&ExpandView"
    host = "http://extranet.aknoe.at"
    urls = []
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for a in root.cssselect("a"):
        if "href" in a.attrib:
            if "OpenDocument" in a.attrib["href"]:
                url = host + a.attrib["href"]
                urls.append(url)
    return(urls)

i = 1
host = "http://extranet.aknoe.at"

for url in get_eintrag_links():
    print "%s: %s" % (i, url)
    i = i+1
    time.sleep(5) # probably needed in order not to get blocked by goo.gl
    try: html = scraperwiki.scrape(url)
    except: continue
    root = lxml.html.fromstring(html)
    print root
    from lxml.html.clean import clean_html
    soup = BeautifulSoup(clean_html(lxml.html.tostring(root)))
    text_parts = soup.findAll(text=True)
    text = '\n'.join(text_parts)
    print text
    attachments = []
    shortattachments = []
    for a in root.cssselect("a"):
        if "href" in a.attrib:
            if "FILE" in a.attrib["href"]:
                attachment = host + a.attrib["href"]
                attachments.append(attachment)
                shortattachments.append(shorten(attachment))

    data = {
      'url' : url,
      'shorturl' : shorten(url),
      'text' : text,
      'attachments' : attachments,
      'shortattachments' : shortattachments
    }

    scraperwiki.sqlite.save(unique_keys=['url'], data=data)