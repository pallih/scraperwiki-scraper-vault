import scraperwiki,re
from BeautifulSoup import BeautifulSoup, SoupStrainer

#Allt er í flokknum Fréttir - óþarfi að leita að því - skilgeinum það þá hér
flokkur = 'Fréttir'

#Array til að geyma fréttadata

frettir = {}

def scrape_safn(url):
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()

        # Forum i gegnum alla tengla sem hafa class=headnews
        frettir = soup.findAll('a', { "class" : "headnews" })
        for a in frettir:
            # Baeta vid leni
            url = 'http://logreglan.is/displayer.asp' + a['href']
            # Saekjum frett med scrape_frett
            scrape_frett(url)


def scrape_frett(url):
    #Athugum hvort við höfum sótt fréttina áður með því að checka á því hvort slóðin hefur metadata
    frett_sed_adur = scraperwiki.metadata.get(url)
    if frett_sed_adur is not None:
        #Ef já - sleppum því að sækja og tilkynnum það
        print "Sleppum frett (sed adur): " + url
        return
    else:
        #Ekki séð frétt áður - vinnum úr henni
        print "Saekjum frett: " + url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()

        #Finnum töfluna með efninu - á undan henni er comment "text area" - sem við notum til að staðsetja okkur
        efni = soup.find(text=re.compile("text area")).findNext('table').table

        
        #Finnum dagsetninguna - það er næsta tr
        date = efni.tr.text
        
        #Setjum dagsetningu og category í array-inn
        frettir['dagsetning'] = date
        frettir['flokkur'] = flokkur
        
        #Finnum fyrirsögn - næsta tr
        fyrirsogn=efni.tr.findNextSibling('tr')
        
        #Setjum fyrirsögn  í array-inn
        frettir['fyrirsogn'] = fyrirsogn.text

        #Finnum meginmál - næsta tr
        content=fyrirsogn.findNextSibling('tr')

        #Setjum meginmál  í array-inn
        frettir['meginmal'] = content.text
        
        #Setjum slóðina í array-inn
        frettir['slod'] = url

        #vistum efnið
        print "vistum frett: " + url
        scraperwiki.datastore.save(["slod"], frettir)
        
        #vistum slodina sem metadata svo við vitum að við séum búin með hana
        scraperwiki.metadata.save(url, '1')
        #print frettir
        
        #Og svo höldum við áfram


        
# Byrjunarsida
start_url = 'http://logreglan.is/displayer.asp?cat_id=1040'

# Setjum spiderinn af stad a rettum stad
scrape_safn(start_url)
