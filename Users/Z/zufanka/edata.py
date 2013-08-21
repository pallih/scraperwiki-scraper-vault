import scraperwiki
import urllib


f = urllib.urlopen('http://v3.sk/~naberacka/edata/missing0.4.csv', 'r')
ico = f.readlines()
#ico = [46342796]


for i in ico:
    print i           
    #website = "http://v3.sk/~naberacka/edata/"+str(i).replace('\n','')
    website = "http://www.edata.sk/ico/"+str(i).replace('\n','')
    #print website
    html = scraperwiki.scrape(website)
    #print html

    import lxml.html           
    root = lxml.html.fromstring(html)
    
    tds = root.cssselect('h2') # get all the <h2> tags
    
    for name in tds:
        if name.text == None:
            #print "Nope"
            continue
        else:
            print str(i).replace('\n','')+','+name.text.replace(',','')                # just the text inside the HTML ta+

            region = root.cssselect("p[class='post-info']")
            print region[0].text.replace('Okres ','')

        #print date_start[x].text

        #for name in tds:
            record = { "id" : str(i).replace('\n','') ,"name" : name.text.replace(',',''), "region" : region[0].text.replace('Okres ','')} # column name and value
            scraperwiki.sqlite.save(["name"], record) # save the records one by one

#//body/div[2]/div/div[1]/h2