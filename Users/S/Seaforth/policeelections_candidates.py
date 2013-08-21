import scraperwiki
import lxml.html    


# Blank Python
mainUrl = "http://www.policeelections.com"


# Blank Python        
html = scraperwiki.scrape(mainUrl + "/forces/")

root = lxml.html.fromstring(html)
count=1
xpath = root.xpath("/html/body/div[@id='container']/div[@id='main']/ul[@class='forcebullets']/li/a")
for a in xpath:
    data = {
            'id' : count,
            'force_name' : a.text_content(),
            'force_name_search': a.text_content().replace(" ","").lower()
        }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data,  table_name="Forces")
    count = count + 1



html = scraperwiki.scrape(mainUrl + "/candidates/")
root = lxml.html.fromstring(html)
count=1

#Pull a list of HREFs for Candidates.
xpath_fragment = root.xpath("/html/body/div[@id='container']/div[@id='main']/ul[@class='mainlatestcands']/li/div[@class='mainlatestcandi']/a/@href")

#if True:
for candidateLink in xpath_fragment:
    htmlNamedCandidate = scraperwiki.scrape(mainUrl + candidateLink + "contact/")
#    htmlNamedCandidate = scraperwiki.scrape("http://www.policeelections.com/candidates/kent/harriet-yeo/contact/")
    rootCandidate = lxml.html.fromstring(htmlNamedCandidate)
    
    name = rootCandidate.xpath("/html/body/div[@id='container']/div[@id='ubermain']/div[@class='left']/h1")[0].text_content()
    
    contactdetails = rootCandidate.xpath("/html/body/div[@id='container']/div[@id='main']/ul[2]/li")
    
    data = {'Id' : count , 'Name' : name.strip()}
    for li in contactdetails:
        contactData = li.text_content().split(":")
        if (contactData.__len__() > 0):
            first = True
            dataValue=""
            for x in contactData:
                if first:
                    dataName=x
                    first=False
                else:
                    if (x.strip() !=''):
                        dataValue+= x.strip()
            
            dataValue = dataValue.replace("mailto:","").replace("Not yet completed.","")

            print(dataValue)
            if dataValue != '':
                data[dataName] = dataValue
        
    scraperwiki.sqlite.save(unique_keys=['Id'], data=data,  table_name="Candidates")
    count = count+1
    print(data)