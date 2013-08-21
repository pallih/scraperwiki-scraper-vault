import lxml.html
import scraperwiki
import re
import datetime
import lxml.etree
from lxml.cssselect import CSSSelector
import urllib2

now = datetime.datetime.now()

def ctext(el):
    result = [ ]
    if el.text:
        result.append(el.text)
    for sel in el:
        assert sel.tag in ["strong", "em", "img", "br", "a", "p", "font"], sel.tag
        result.append(ctext(sel))
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


def Parse():
    tdata = scraperwiki.sqlite.select("* from pages order by scrapedate limit 300")
    for t in tdata:
        data = { "url":t["url"] }

        root = lxml.html.fromstring(t["content"])
        data["name"] = root.cssselect("div#cit h1")[0].text

        img = root.cssselect("img")[0]
        data["image"] = "http://www.meclis.gov.az/" + img.attrib.get("src")
        
        for p in list(root.cssselect("div#mod_senter_text")[0]):
            s = ctext(p)
            mdistrict = re.match(u'\xa0?(\d+)[\xa0\s]+sayl\xc4\xb1[\xa0 ]+(.*)', s)
            mdob = re.match(u'Do\xc4\x9fum ili:\s+(\d\d\d\d)', s)
            mparty = re.match(u'Partiya[\xa0 ]+m\xc9\x99nsubiyy\xc9\x99ti:[\xa0 ]+(.*)', s)
            if mdistrict:
                data["district_number"] = mdistrict.group(1)
                data["district_name"] = mdistrict.group(2)
            elif mdob:
                data["dob"] = mdob.group(1)
            elif mparty:
                data["party"] = mparty.group(1)
            elif re.match("\s*<p>\s*<a href=\?/az/ask/deputat/>Deputatdan", s):
                pass
            elif not s.strip():
                pass
            else:
                print t["url"], [s]
            scraperwiki.sqlite.save(["url"], data=data, table_name="deputies")

def Scrape():
    url = "http://www.meclis.gov.az/?/az/deputat/"
    x = urllib2.urlopen(url).read().decode("utf8")
    root = lxml.html.fromstring(x)
    options = root.cssselect("div#mod_senter_text option")
    for option in options:
        #print  option.text,option.attrib.get("value")

        if option.attrib.get("value"):
            durl = "http://www.meclis.gov.az/?/az/deputat/"+option.attrib.get("value")
            x1 = urllib2.urlopen(durl).read().decode("utf8")
            droot = lxml.html.fromstring(x1)
            content = droot.cssselect("div#mod_center")
            data = {"url":durl,"value":option.attrib.get("value"), "scrapedate":now}
            data["content"] = lxml.html.tostring(content[0])
            scraperwiki.sqlite.save(["value", "content"], data, table_name="pages")

#Scrape()
Parse()