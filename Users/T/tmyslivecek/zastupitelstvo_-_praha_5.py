import scraperwiki
import lxml.html
import sys

try:
    html = scraperwiki.scrape("http://www.praha5.cz/cs/sekce/usneseni-zastupitelstva/")
    root = lxml.html.fromstring(html)
except:
    print "Unexpected error:", sys.exc_info()[0]


for li in root.cssselect("ul li"):
    for a in li.cssselect("a"):
        ahref = a.attrib['href']
        if "/cs/zasedani/usneseni-zastupitelstva/" in ahref:

            try:
                html2 = scraperwiki.scrape("http://www.praha5.cz"+ahref)
                root2 = lxml.html.fromstring(html2)
            except:
                print "Unexpected error:", sys.exc_info()[0]
            

            for tr in root2.cssselect("table.tabular tr"):
                tds = tr.cssselect("td")
                if len(tds)==4:
                    for a1 in tds[3].cssselect("a"):
                        ahref1 = a1.attrib['href']

                        try:
                            html3 = scraperwiki.scrape("http://www.praha5.cz"+ahref1)
                            root3 = lxml.html.fromstring(html3)
                        except:
                            print "Unexpected error:", sys.exc_info()[0]

                        for div in root3.cssselect("div.middle"):
                            data = {
                                'id_zapis' : ahref1[ahref1.rfind("/")+1:],
                                'zapis' : div.text_content().encode('utf-8')
                            }
                            scraperwiki.sqlite.save(unique_keys=['id_zapis'], data=data)

            list1 = []
            for a3 in root2.cssselect("div.paginationControl a"):
                list1.append(a3.attrib['href'])
            if len(list1)>2:
                list1.pop()
                list1.pop()
                for listitem in list1:
    
                    html3 = scraperwiki.scrape("http://www.praha5.cz"+ahref)
                    root3 = lxml.html.fromstring(html3)
                    
        
                    for tr in root3.cssselect("table.tabular tr"):
                        tds = tr.cssselect("td")
                        if len(tds)==4:
                            for a1 in tds[3].cssselect("a"):
                                ahref1 = a1.attrib['href']
        
                                html4 = scraperwiki.scrape("http://www.praha5.cz"+ahref1)
                                root4 = lxml.html.fromstring(html4)
        
                                for div in root4.cssselect("div.middle"):
                                    data = {
                                        'id_zapis' : ahref1[ahref1.rfind("/")+1:],
                                        'zapis' : div.text_content().encode('utf-8')
                                    }
                                    scraperwiki.sqlite.save(unique_keys=['id_zapis'], data=data)
