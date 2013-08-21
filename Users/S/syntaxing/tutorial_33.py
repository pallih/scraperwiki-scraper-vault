import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://slickdeals.net/forums/forumdisplay.php?f=9&page=1&order=desc&sort=lastpost")
root = lxml.html.fromstring(html)


#print root.cssselect("div.threadtitleline a")
for el in root.cssselect("div.threadtitleline a"):
    if el.text == None or el.text == '\r\n' :
        pass
    if (el.text == '1' or el.text == '2' or el.text == '3' or el.text == '4' or el.text == '5'):
        pass

    else:     
        print el.text
        #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el.text, "bbb":el.attrib['href']})

    #print lxml.html.tostring(el)

    #print el.attrib['href']

