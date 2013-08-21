import scraperwiki
import lxml.html
data={}
for i in range(2006,2013):  
    url = "http://federalreserve.gov/newsevents/speech/"+str(i)+"speech.htm"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    root.make_links_absolute(url)
    links = root.cssselect("#speechIndex a")
    for link in links:
        speechUrl = link.get("href")
        speechHtml = scraperwiki.scrape(speechUrl)
        speechRoot = lxml.html.fromstring(speechHtml)
        links = speechRoot.cssselect("a")
        for link in links:
            link.drop_tree()
        date_el = speechRoot.cssselect(".speechDate")
        if len(date_el)>0:
            date = speechRoot.cssselect(".speechDate")[0].text_content().lstrip().rstrip()
            full_text=""
            for paragraph in speechRoot.cssselect("p"):
                text = paragraph.text_content()
                if not ("Return to top" in text or text.isspace()):
                    full_text+=text+" "
            if date in data:
                data[date]+=full_text
            else:
                data[date]=full_text
        else:
            print "Omission. Unexpected Format"
#list of dicts
lod = []
for k,v in data.iteritems():
    lod.append({"date":k,"text":v})
scraperwiki.sqlite.save(["date"],lod)
