import lxml.html, urllib2, re, scraperwiki

url = "http://www.slv.se/sv/grupp1/Markning-av-mat/Tillsatser-i-mat/E-nummernyckeln---godkanda-tillsatser/"
html = urllib2.urlopen(url).read()
html = html[html.find("<!DOCTYPE"):]
root = lxml.html.fromstring(html)

def extract_text(el):
    s = ""
    for e in el.itertext():
        s += e
    return s.strip()

headings = root.cssselect("h2")
print "There are %d elements with tag h2 in this page" % len(headings)
print "Their corresponding attributes are:", [extract_text(div) for div in headings]


for h in headings:
    grouping = extract_text(h)
    try:
        es = h.getnext().cssselect("tr")
    except:
        es = []
    for e in es:
        code, name = extract_text(e[0]), extract_text(e[1])
        data = { 'code': code, 'name': name, 'grouping': grouping }
        scraperwiki.sqlite.save(unique_keys=['code'], data=data)
        