import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")
#dictionary openen
scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")
#url pakken als kenmerk per record en printen zodat je ziet als er iets misgaat
for scraping in scrapings:
    url = scraping["URL"]
    print url
    #nu de html pakken
    soup = BeautifulSoup(scraping["HTML"])
    #en de onderdelen; haal language option weg (replace pakt alleen de eerste) en strip spaties en tabs en zo
    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()

    details = soup.find_all("div", "inner maintext")
    counter = 1

    for detail in details:
        RefNum = [2]
        EstLen = [3]
        AwValu = [4]
        LocCon = [5]
        NamBuy = [6]        
                
        data = {"URL": url, "id": counter} #om een unieke id te maken per record
        scraperwiki.sqlite.save(["URL"], data)
        counter+=1 #telt de counter op
print title
print detailsimport scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")
#dictionary openen
scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")
#url pakken als kenmerk per record en printen zodat je ziet als er iets misgaat
for scraping in scrapings:
    url = scraping["URL"]
    print url
    #nu de html pakken
    soup = BeautifulSoup(scraping["HTML"])
    #en de onderdelen; haal language option weg (replace pakt alleen de eerste) en strip spaties en tabs en zo
    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()

    details = soup.find_all("div", "inner maintext")
    counter = 1

    for detail in details:
        RefNum = [2]
        EstLen = [3]
        AwValu = [4]
        LocCon = [5]
        NamBuy = [6]        
                
        data = {"URL": url, "id": counter} #om een unieke id te maken per record
        scraperwiki.sqlite.save(["URL"], data)
        counter+=1 #telt de counter op
print title
print details