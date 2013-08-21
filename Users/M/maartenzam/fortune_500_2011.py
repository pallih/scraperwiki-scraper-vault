import scraperwiki
import lxml.html 

# Blank Python

rooturl = "http://money.cnn.com/magazines/fortune/global500/2011/full_list/"
pages = ("","101_200.html","201_300.html","301_400.html","401_500.html")

for page in pages:
    html = scraperwiki.scrape(rooturl+page)
    print html
          
    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("table.cnnwith220inset tr"):
        profilelink = tr.cssselect("a")[0].get("href").replace("..","http://money.cnn.com/magazines/fortune/global500/2011")
        #companyhtml = scraperwiki.scrape(profilelink)
        #companyroot = lxml.html.fromstring(companyhtml)
        #companydata = companyroot.cssselect("div.snapUniqueData b")[1]
        #companydatatext= companydata
        #print companydatatext
        
        data = {
          'rank' : tr[0].text_content(),
          'company' : tr[1].text_content(),
          'revenues' : tr[2].text_content(),
          'profits' : tr[3].text_content(),
          'profileurl' : profilelink,
          #'companydata' : companydatatext
        }
        scraperwiki.sqlite.save(unique_keys=['company'], data=data)

    #print tds