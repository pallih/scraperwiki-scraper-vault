import scraperwiki
import lxml.html
urllast = "/language/en-US/Default.aspx"
import re
national = ["5081", 17]
london = ["4943", 7, "london"]
southeast = ["5381", 8, "southeast"]
southwest = ["5444", 6, "southwest"]
east = ["5496", 6, "east"]
eastmidlands = ["5526", 6, "eastmidlands"]
westmidlands = ["5556", 6, "westmidlands"]
wales = ["5604", 6, "wales"]
yorkshire = ["5634", 6, "yorkshire"]
northwest = ["5664", 6, "northwest"]
northeast = ["5694", 6, "northeast"]
ni = ["6081", 5, "ni"]
scotland = ["5736",6, "scotland"]

urllondon = "http://www.cvqo.org/dnn/2/Regions/London/RegionalNewsLondon/tabid/2042/currentpage/"
urlsoutheast = "http://www.cvqo.org/dnn/2/Regions/SouthEast/RegionalNewsSouthEast/tabid/2281/currentpage/"
urlsouthwest = "http://www.cvqo.org/dnn/2/Regions/SouthWest/RegionalNewsSouthWest/tabid/2304/currentpage/"
urleast = "http://www.cvqo.org/dnn/2/Regions/EastofEngland/RegionalNewsEastofEngland/tabid/2343/currentpage/"
urleastmidlands = "http://www.cvqo.org/dnn/2/Regions/EastMidlands/RegionalNewsEastMidlands/tabid/2347/currentpage/"
urlwestmidlands = "http://www.cvqo.org/dnn/2/Regions/WestMidlands/RegionalNewsWestMidlands/tabid/2351/currentpage/"
urlwales = "http://www.cvqo.org/dnn/2/Regions/Wales/RegionalNewsWales/tabid/2364/currentpage/"
urlyorkshire = "http://www.cvqo.org/dnn/2/Regions/YorkshireandHumber/RegionalNewsYorkandHumber/tabid/2368/currentpage/"
urlnorthwest = "http://www.cvqo.org/dnn/2/Regions/NorthWest/RegionalNewsNorthWest/tabid/2372/currentpage/"
urlnortheast = "http://www.cvqo.org/dnn/2/Regions/NorthEast/RegionalNewsNorthEast/tabid/2376/currentpage/"
urlni = "http://www.cvqo.org/dnn/2/Regions/NorthernIreland/RegionalNewsNorthernIreland/tabid/2542/currentpage/"
urlscotland = "http://www.cvqo.org/dnn/2/Regions/Scotland/RegionalNewsScotland/tabid/2403/currentpage/"


#setup where we are
urlfirst = urlscotland
regionid = scotland[0]
regionindex = scotland[1]
region = scotland[2]

def addRow(thehtml, tag, divno, region):
    #print tag
    for singletag in thehtml.cssselect(tag):
        title = singletag.text_content().strip()
        div = root.cssselect("div.normal")[divno]
        intro = div.text_content().strip()
        intro = intro.strip()
        if 'href' in singletag.attrib:
            link = singletag.attrib['href']
            body = ""
        else:
            link = "#"
            body = intro
        scraperwiki.sqlite.save(unique_keys=[], data={"title":title, "link":link, "intro":intro, "body":body, "region":region}, table_name="regional_news")

for urlpage in range (1, regionindex):
    #print "number %d" % (urlpage)
    html = scraperwiki.scrape(urlfirst + str(urlpage) + urllast)
    root = lxml.html.fromstring(html)
    for index in range (0, 4):
        addRow(root, "a#dnn_ctr" + regionid + "_ArticleList_ctl00_lstArticles_ctl0" + str(index) + "_titleLink", index, region)

import scraperwiki
import lxml.html
urllast = "/language/en-US/Default.aspx"
import re
national = ["5081", 17]
london = ["4943", 7, "london"]
southeast = ["5381", 8, "southeast"]
southwest = ["5444", 6, "southwest"]
east = ["5496", 6, "east"]
eastmidlands = ["5526", 6, "eastmidlands"]
westmidlands = ["5556", 6, "westmidlands"]
wales = ["5604", 6, "wales"]
yorkshire = ["5634", 6, "yorkshire"]
northwest = ["5664", 6, "northwest"]
northeast = ["5694", 6, "northeast"]
ni = ["6081", 5, "ni"]
scotland = ["5736",6, "scotland"]

urllondon = "http://www.cvqo.org/dnn/2/Regions/London/RegionalNewsLondon/tabid/2042/currentpage/"
urlsoutheast = "http://www.cvqo.org/dnn/2/Regions/SouthEast/RegionalNewsSouthEast/tabid/2281/currentpage/"
urlsouthwest = "http://www.cvqo.org/dnn/2/Regions/SouthWest/RegionalNewsSouthWest/tabid/2304/currentpage/"
urleast = "http://www.cvqo.org/dnn/2/Regions/EastofEngland/RegionalNewsEastofEngland/tabid/2343/currentpage/"
urleastmidlands = "http://www.cvqo.org/dnn/2/Regions/EastMidlands/RegionalNewsEastMidlands/tabid/2347/currentpage/"
urlwestmidlands = "http://www.cvqo.org/dnn/2/Regions/WestMidlands/RegionalNewsWestMidlands/tabid/2351/currentpage/"
urlwales = "http://www.cvqo.org/dnn/2/Regions/Wales/RegionalNewsWales/tabid/2364/currentpage/"
urlyorkshire = "http://www.cvqo.org/dnn/2/Regions/YorkshireandHumber/RegionalNewsYorkandHumber/tabid/2368/currentpage/"
urlnorthwest = "http://www.cvqo.org/dnn/2/Regions/NorthWest/RegionalNewsNorthWest/tabid/2372/currentpage/"
urlnortheast = "http://www.cvqo.org/dnn/2/Regions/NorthEast/RegionalNewsNorthEast/tabid/2376/currentpage/"
urlni = "http://www.cvqo.org/dnn/2/Regions/NorthernIreland/RegionalNewsNorthernIreland/tabid/2542/currentpage/"
urlscotland = "http://www.cvqo.org/dnn/2/Regions/Scotland/RegionalNewsScotland/tabid/2403/currentpage/"


#setup where we are
urlfirst = urlscotland
regionid = scotland[0]
regionindex = scotland[1]
region = scotland[2]

def addRow(thehtml, tag, divno, region):
    #print tag
    for singletag in thehtml.cssselect(tag):
        title = singletag.text_content().strip()
        div = root.cssselect("div.normal")[divno]
        intro = div.text_content().strip()
        intro = intro.strip()
        if 'href' in singletag.attrib:
            link = singletag.attrib['href']
            body = ""
        else:
            link = "#"
            body = intro
        scraperwiki.sqlite.save(unique_keys=[], data={"title":title, "link":link, "intro":intro, "body":body, "region":region}, table_name="regional_news")

for urlpage in range (1, regionindex):
    #print "number %d" % (urlpage)
    html = scraperwiki.scrape(urlfirst + str(urlpage) + urllast)
    root = lxml.html.fromstring(html)
    for index in range (0, 4):
        addRow(root, "a#dnn_ctr" + regionid + "_ArticleList_ctl00_lstArticles_ctl0" + str(index) + "_titleLink", index, region)

