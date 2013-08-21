import scraperwiki,re
from BeautifulSoup import BeautifulSoup, SoupStrainer

#Allt er í flokknum Lausar stöður - óþarfi að leita að því - skilgeinum það þá hér
flokkur = 'Lausar stöður'

#Array til að geyma fréttadata

lausar_stodur = {}


def scrape_month(url):
        #Vinnum manadar archive
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()

        # Forum i gegnum alla tengla sem hafa class=headnews
        frettir = soup.findAll('a', { "class" : "headnews" })
        for a in frettir:
            # Baeta vid leni
            url = 'http://logreglan.is/' + a['href']
            # Saekjum frett med scrape_frett
            print url
            scrape_ad(url)

def scrape_months(url):
        #Manudir
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()

        td = soup.findAll('td', { "style" : "padding-left:10px" })
        for a in td:
            link = a.findAll('a')
            for a in link:
                url = 'http://logreglan.is/' + a['href']
                print ">>>>****<<<< Vinnum manud - : " + url

                scrape_month(url)


def scrape_ad(url):
    #Athugum hvort við höfum sótt fréttina áður með því að checka á því hvort slóðin hefur metadata
    ad_sed_adur = scraperwiki.metadata.get(url)
    if ad_sed_adur is not None:
        #Ef já - sleppum því að sækja og tilkynnum það
        print "Sleppum auglysingu (sed adur): " + url
        return
    else:
        #Ekki séð frétt áður - vinnum úr henni
        print "Saekjum auglysingu: " + url
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        soup.prettify()

        #Finnum töfluna með efninu - á undan henni er comment "text area" - sem við notum til að staðsetja okkur
        efni = soup.find(text=re.compile("text area")).findNext('table').table

        
        #Finnum dagsetninguna - það er næsta tr
        date = efni.tr.text
        
        #Setjum dagsetningu og category í array-inn
        lausar_stodur['dagsetning'] = date
        lausar_stodur['flokkur'] = flokkur
        
        #Finnum fyrirsögn - næsta tr
        fyrirsogn=efni.tr.findNextSibling('tr')
        
        #Setjum fyrirsögn  í array-inn
        lausar_stodur['fyrirsogn'] = fyrirsogn.text

        #Finnum meginmál - næsta tr
        content=fyrirsogn.findNextSibling('tr')

        #Setjum meginmál  í array-inn
        lausar_stodur['meginmal'] = content.text
        
        #Setjum slóðina í array-inn
        lausar_stodur['slod'] = url

        #vistum efnið
        print "vistum auglysingu: " + url
        scraperwiki.datastore.save(["slod"], lausar_stodur)
        
        #vistum slodina sem metadata svo við vitum að við séum búin með hana
        scraperwiki.metadata.save(url, '1')
        print lausar_stodur
        
        #Og svo höldum við áfram


        
# Byrjunarsida
start_url = 'http://logreglan.is/default.asp?cat_id=959'

# Setjum spiderinn af stad a rettum stad
scrape_months(start_url)
