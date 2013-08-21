import scraperwiki
import lxml.html


#
# Informazioni sugli stati della UE
#

# Test Python
print "Informazioni sugli stati della UE"


# Download HTML from the web
html = scraperwiki.scrape("http://eeas.europa.eu/delegations/switzerland/what_eu/eu_memberstates/index_it.htm")
#print html


# Parsing the HTML to get content and  Saving to the ScraperWiki datastore
root = lxml.html.fromstring(html)
count = -1
for tr in root.cssselect("div[class='cont'] table[class='tableDefault']  table[class='tableDefault'] tr"):
        count = count+1
        print count

        tds = tr.cssselect("td")
        flagimg = tds[0].cssselect("img")
        xhtml = lxml.html.document_fromstring(html)
        flagImageURL = xhtml.xpath('//table[@class="tableDefault"]//table[@class="tableDefault"]//img/@src')
        detailPageURL = xhtml.xpath('//table[@class="tableDefault"]//table[@class="tableDefault"]//a/@href')

        # Processa la pagina dei dettagli
        htmlDetails = scraperwiki.scrape(detailPageURL[count])
        root2 = lxml.html.fromstring(htmlDetails)
        detailsDiv = root2.cssselect("div[class='countries_infos member_countries']")[0]

        countDetails = 0
        detailsArray = [0,0,0,0,0,0]
        for detailsP in detailsDiv.cssselect("p"):
            if countDetails==2 :
                tmp = detailsP.text_content().split(":")[1].strip()
                last = len(tmp)-3
                detailsArray[countDetails]=tmp[0:last].replace(' ','')
            elif countDetails==3 :
                tmp = detailsP.text_content().split(":")[1].strip()
                last = len(tmp)-len('milioni')
                detailsArray[countDetails]=tmp[0:last].strip().replace(',','.')
            else :
                detailsArray[countDetails]=detailsP.text_content().split(":")[1]
#            print detailsP.text_content().split(":")[0], "  :  ", detailsP.text_content().split(":")[1], detailsArray[countDetails]
            countDetails = countDetails + 1

        # Crea la struttura dati dle singolo record
        data = {
            'country' : tds[1].text_content().strip(),
            'flagImageURL': 'http://eeas.europa.eu'+flagImageURL[count],
            'detailPageURL': detailPageURL[count],
            'details' : detailsDiv.text_content(),
            'anno_adesione': detailsArray[0],
            'capitale': detailsArray[1],
            'superficie': detailsArray[2],
            'popolazione': detailsArray[3],
            'valuta': detailsArray[4],
            'schenghen': detailsArray[5]
        }

        # Salva i dati
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

        # Stampa il dato a video
#        print data['country'] + " - " + data['flagImageURL'] + " - " + data['detailPageURL'] + " - " + data['details']
#        print data['anno_adesione'] + ", " + data['capitale'] + ", " + data['superficie'] + ", " + data['popolazione'] + ", " + data['valuta'] + ", " + data['schenghen']

# Riepilogo 
print "Paesi della UE: " , count+1


