import scraperwiki
import re
import lxml.html
from lxml.html.clean import clean_html

snippets = []

# Blank Python
for i in range(200,3001):
    url = "http://africancso.org/cso-sign-up?pageAction=view&selected_organization_id="+str(i)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    print clean_html(html)
    for el in root.cssselect("div.portlet-msg-error"):
        print el.text

    for el in root.cssselect("td.Label"):
        print el.text

def ctext(el):
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        assert sel.tag in ["p", "span","div"]
        result.append("<"+sel.tag+">")
        result.append(ctext(sel))
        result.append("</"+sel.tag+">")
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


html = scraperwiki.scrape("http://www.refc.com.ph/index.php?q=page/investors")
root = lxml.html.fromstring(html)
snippets = []
n=0

for el in root.cssselect("a.imagecache-Investors-icon"):
    print el
    htmlIn = scraperwiki.scrape("http://www.refc.com.ph"+el.attrib['href'])
    rootIn = lxml.html.fromstring(htmlIn)
    for elIn in rootIn.cssselect("div.content.clear-block"):
        focalpoint = lxml.html.tostring(elIn)
        if len(elIn.cssselect("img")) > 0:
            focalimg = elIn.cssselect("img")[0].attrib['src']
        if len(elIn.cssselect("p")) > 0:
            focalp = lxml.html.tostring( elIn.cssselect("p")[0])
            focaltitle = elIn.cssselect("p")[0].text.strip(' \t\n\r')
        #print re.subn(r'<p>(.*?)<br>','$1',focalpoint)
        snippets.append({"num":n,"html":focalpoint,"img":focalimg, "p":focalp, "title":focaltitle})
        print focalpoint;
        n=n+1

scraperwiki.sqlite.save(unique_keys=["num"],data=snippets)
print scraperwiki.sqlite.show_tables()
print scraperwiki.sqlite.execute("select * from swdata") 
