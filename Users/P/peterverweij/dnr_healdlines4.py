import scraperwiki
import lxml
base = "http://denieuwereporter/page/"
for num in range(0,10):
    pagename = base + str(num)
    url = pagename
    print url
    page = scraperwiki.scrape(url)
    #pageroot = lxml.html.fromstring(url)
    #for hl in pageroot.csselect("h1"):
     #   hl = h1.text_content()
    #print hl

