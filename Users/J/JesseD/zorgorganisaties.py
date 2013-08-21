import scraperwiki
import lxml.html 

# Blank Python
count = 1
while (count < 34):
    html = scraperwiki.scrape("http://www.kiesbeter.nl/ziekte-en-gezondheid/zoeken/trefwoord/patientenorganisaties/a/pagina/"+str(count)+"/")         
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    
    divs = root.cssselect("div.bd")   # get all the <div> tags with class='db'
    for div in divs:
        hrefs = div.cssselect("a['href']")    # get all the <a> tags
        href = hrefs[1]
        hreftext = href.text    # remove '- patiëntorganisaties' from string
        #data = {
        #    'organisatie' : organisation
        #}
        #scraperwiki.sqlite.save(unique_keys=['organisatie'], data=data)
        #print "http://www.kiesbeter.nl/"+hreftext
        instellinglink = "http://www.kiesbeter.nl/"+hreftext
        instellinghtml = scraperwiki.scrape(instellinglink )
        instellingroot = lxml.html.fromstring(instellinghtml) # turn our zorginstelling HTML into an lxml object
        contacttable = instellingroot.cssselect("div.tab tbody")
        for tbody in contacttable:
            tr = tbody.cssselect("tr")
            #mail = tr[1].cssselect("td")[0].text_content() #haalt nu nog TWEE EMAILS op en plakt ze aan elkaar
            aands = tr[8].cssselect("td ul li")            
            countaand = 0
            aandstring = "";            
            for aand in aands:
                if countaand == 0:
                    aandstring = "-" + aand.text_content()                
                    countaand = countaand + 1
                elif countaand > 0:
                    aandstring = aandstring + "<br>-" + aand.text_content()
            if len(aands) == 0:
                aandsingle = tr[8] #tr[8].cssselect("td")
                aandstring = aandsingle[1].text_content()
                if aandstring == "":
                    aandstring = "-"
            data = {
                'aandachtsgebieden' : aandstring
            }
            scraperwiki.sqlite.save(unique_keys=['aandachtsgebieden'], data=data)
            #print aandstring
    count = count + 1