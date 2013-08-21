import scraperwiki
import lxml.etree
import lxml.html

def scrapeTable(root):

    #détail joueur
    marketValue=''
    contract=''
    agent=''

    detailsJoueur= root.cssselect("td.al table.tabelle_spieler tr")
    
    for detailJoueur in detailsJoueur:
        #print detailJoueur[0].text.split("’")[0]

        #print detailJoueur[0].cssselect("td")[1].text
        if detailJoueur[0].text =="Valeur marchande:":
            marketValue=detailJoueur[1].text

        #elif detailJoueur[0].text=="Contrat jusqu/’en:":
        #    contract=detailJoueur[1].text

        elif detailJoueur[0].text=="Agent de joueurs:":
            agent=detailJoueur[1].text

        contract=detailJoueur[1].text

    #enregistrement des resultats
    record = {}

    record["teamName"]=teamName
    record["nomJoueur"]= nomJoueur
    record["marketValue"]= marketValue
    record["contract"]= contract
    record["agent"]= agent

    #save in datastore
    scraperwiki.sqlite.save(["teamName", "nomJoueur"], record)

#start
sUrlBase="http://www.transfermarkt.fr/fr/ligue-1/startseite/wettbewerb_FR1.html"

html = scraperwiki.scrape(sUrlBase)
rootClub = lxml.html.fromstring(html)

#recupère les lien vers tous les joueurs
aClubs=rootClub.cssselect("table#vereine td.ac a")

for club in aClubs:

    #nom du club
    teamName=club.attrib['href'].split("/")[2]
    
    html = scraperwiki.scrape("http://www.transfermarkt.fr"+ club.attrib['href'])
    rootJoueur = lxml.html.fromstring(html)

    #liste de l'ensemble des joueurs d'un club
    aJoueur=rootJoueur.cssselect("table#spieler tr a")

    #boucle sur les joueurs
    for joueur in aJoueur:

        #nom du joueur
        nomJoueur=joueur.text

        html = scraperwiki.scrape("http://www.transfermarkt.fr"+ joueur.attrib['href'])
        root = lxml.html.fromstring(html)
        scrapeTable(root)  
