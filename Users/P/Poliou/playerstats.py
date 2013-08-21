import scraperwiki
import lxml.etree
import lxml.html
import datetime
import types

def scrapeTable(root):
    
    #nomJoueur
    nomJoueur=root.cssselect("div.nwIdentity h1")[0]
    #nbMatches
    nbMatches=root.cssselect("div.nwStat tbody tr td strong")[0]
    #nbTitulaires
    nbTitulaires=root.cssselect("div.nwStat tbody tr td strong")[1]
    #tempsJeu
    tempsJeu=root.cssselect("div.nwStat tbody tr td strong")[2]
    #Buts
    nbButs=root.cssselect("div.nwStat tbody tr td strong")[3]
    #CartonsJaunes
    cartonsJaunes=root.cssselect("div.nwStat tbody tr td strong")[4]
    #cartonsRouges
    cartonsRouges=root.cssselect("div.nwStat tbody tr td strong")[5]
    #note joueur
    note=''
    if len(root.cssselect("div.nwNote strong"))!=0:
        noteJoueur=root.cssselect("div.nwNote strong")[0]
        note=noteJoueur.text

    #détail joueur
    posteJoueur=''
    dob=''

    detailsJoueur= root.cssselect("div.nwIdentity ul li")
    
    for detailJoueur in detailsJoueur:
        if detailJoueur.cssselect("span")[0].text=="Poste : ":
            posteJoueur=detailJoueur.cssselect("b")[0].text
            
        elif detailJoueur.cssselect("span")[0].text=="Date de naissance: ":
            dob=detailJoueur.cssselect("b")[0].text

            
    #enregistrement des resultats
    record = {}

    record["teamName"]=teamName.text
    record["nomJoueur"]= nomJoueur.text
    record["nbMatches"]= nbMatches.text
    record["nbTitulaires"]= nbTitulaires.text       
    record["tempsJeu"]= tempsJeu.text   
    record["nbButs"]= nbButs.text  
    record["cartonsJaunes"]= cartonsJaunes.text  
    record["cartonsRouges"]= cartonsRouges.text
    record["noteJoueur"]= note
    record["dateNaissance"]= dob
    record["poste"]= posteJoueur
    record["nbPointsClub"]=nbPointsClub.text

    #save in datastore
    scraperwiki.sqlite.save(["teamName", "nomJoueur"], record)

#start
sUrlBase="http://www.sports.fr/football/ligue-1/2012/classements/classement-general.html"

html = scraperwiki.scrape(sUrlBase)
rootClub = lxml.html.fromstring(html)

#recupère les lien vers tous les clubs
aClubs=rootClub.cssselect("div.nwTable table tbody.tc tr")


#boucle sur tous les clubs
for club in aClubs:

    nbPointsClub=club.cssselect("td.alt")[0]

    #sURL= sUrlBase+ club.attrib['href']
    html = scraperwiki.scrape("http://www.sports.fr"+ club.cssselect("a")[0].attrib['href'])

    rootClub = lxml.html.fromstring(html)

    #Team Name
    teamName=rootClub.cssselect("div.nwIdentity h1")[0]
    
    #liste de l'ensemble des joueurs d'un club
    aJoueur=rootClub.cssselect("div#right div.nwTable table a")
    
    #boucle sur tous les joueurs
    for joueur in aJoueur:
        
        print "http://www.sports.fr" + joueur.attrib['href']

        #lienJoueur=rootClub.cssselect("a.lien_fiche")
        html = scraperwiki.scrape("http://www.sports.fr" + joueur.attrib['href'])
        root = lxml.html.fromstring(html)
        
        scrapeTable(root)   

