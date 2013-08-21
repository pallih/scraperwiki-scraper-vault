import scraperwiki
import lxml.html


for i in range(2001,2006):
    data={}
    print i
    url = "http://federalreserve.gov/newsevents/speech/"+str(i)+"speech.htm"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    root.make_links_absolute(url)
    links = root.cssselect("#speechIndex a")
    for link in links:
        speechUrl = link.get("href")
        date = link.text_content().strip()
        speechHtml = scraperwiki.scrape(speechUrl)
        speechRoot = lxml.html.fromstring(speechHtml)
        mylinks = root.cssselect("a")
        for link in mylinks:
            link.drop_tree()
        paras = speechRoot.cssselect("td")
        text = ""
        for elem in paras:
            text+=" "+elem.text_content()
        text = text[text.find(date)+len(date):]
        if date in data:
            data[date]+=text
        else:
            data[date]=text
    lod = []
    for k,v in data.iteritems():
        lod.append({"date":k,"text":v})
    scraperwiki.sqlite.save(["date"],lod)
