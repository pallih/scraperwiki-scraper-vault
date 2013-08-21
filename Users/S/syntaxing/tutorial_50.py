import scraperwiki
import lxml.html

for x in xrange(1,5):    
    url = "http://slickdeals.net/forums/forumdisplay.php?f=9&page=" + str(x) + "&order=desc&sort=lastpost"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    
    #print root.cssselect("div.threadtitleline a")
    for el in root.cssselect("div.threadtitleline a"):
        while True:
            if el.text == None or el.text == ' ' or el.text=='Last Page' :
                break
            if (el.text == '1' or el.text == '2' or el.text == '3' or el.text == '4' or el.text == '5'):
                break
    
            else: 
                scraperwiki.sqlite.save(unique_keys=["title"], data={"title":el.text, "link": el.attrib['href']})   
                print el.text
                break
        
                #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el.text, "bbb":el.attrib['href']})
        
                #print lxml.html.tostring(el)
            
                #print el.attrib['href']

