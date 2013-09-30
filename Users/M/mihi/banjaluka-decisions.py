import scraperwiki
import lxml.html
import re

# Blank Python

base="http://sgbl.banjaluka.rs.ba/rsg/klijent/"

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_announcements(year):
    root=get_root("http://sgbl.banjaluka.rs.ba/rsg/klijent/brojevi.php?id_godina=%s"%year)
    announces=root.xpath("//div[3]/div[2]/ul/li/a")
    return ["%s%s"%(base,i.attrib["href"]) for i in announces]

def get_decisions(url):
    root=get_root(url)
    decisions=root.xpath("//div[3]/div[2]/ul/li/a")
    return ["%s%s"%(base,i.attrib["href"]) for i in decisions]

def get_protocolno(text):
    for i in text:
        pno=re.search("([0-9]+-[0-9]+-[0-9]+/[0-9]{2,4}\.)",i)
        if pno:
            return pno.group(1)

def get_act(url):
    root=get_root(url)
    title=root.cssselect("#main > h1")[0].text_content()
    text=[i.text_content() for i in root.cssselect("#main > div > p")]
    header=text[1]
    date=re.search("([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})",header)
    if date:
        date=date.group(1)
    else:
        date=None
    fulltext="\n".join(text)
    protocolno=get_protocolno(text)
    scraperwiki.sqlite.save(unique_keys=["URL"],data={"title":title, "URL":url, "text":fulltext, "date":date,"protocolno":protocolno})

years=range(2002,2014)
for year in years:
    for a in get_announcements(year):
        for d in get_decisions(a):
            get_act(d)
import scraperwiki
import lxml.html
import re

# Blank Python

base="http://sgbl.banjaluka.rs.ba/rsg/klijent/"

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_announcements(year):
    root=get_root("http://sgbl.banjaluka.rs.ba/rsg/klijent/brojevi.php?id_godina=%s"%year)
    announces=root.xpath("//div[3]/div[2]/ul/li/a")
    return ["%s%s"%(base,i.attrib["href"]) for i in announces]

def get_decisions(url):
    root=get_root(url)
    decisions=root.xpath("//div[3]/div[2]/ul/li/a")
    return ["%s%s"%(base,i.attrib["href"]) for i in decisions]

def get_protocolno(text):
    for i in text:
        pno=re.search("([0-9]+-[0-9]+-[0-9]+/[0-9]{2,4}\.)",i)
        if pno:
            return pno.group(1)

def get_act(url):
    root=get_root(url)
    title=root.cssselect("#main > h1")[0].text_content()
    text=[i.text_content() for i in root.cssselect("#main > div > p")]
    header=text[1]
    date=re.search("([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})",header)
    if date:
        date=date.group(1)
    else:
        date=None
    fulltext="\n".join(text)
    protocolno=get_protocolno(text)
    scraperwiki.sqlite.save(unique_keys=["URL"],data={"title":title, "URL":url, "text":fulltext, "date":date,"protocolno":protocolno})

years=range(2002,2014)
for year in years:
    for a in get_announcements(year):
        for d in get_decisions(a):
            get_act(d)
