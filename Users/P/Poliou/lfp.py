import scraperwiki
import lxml.etree
import lxml.html
from datetime import date

def scrapeTable(root):

    nbButsEncaisses=''
    posteJoueur=''
    dobJoueur=''

    #nom du joueur
    nomJoueur=root.cssselect("div#fiche h1")[0].text

    #poste du joueur
    detailsJoueur=root.cssselect("div.infos_joueur dl dd")

    for detailJoueur in detailsJoueur:
        if(detailJoueur.text=='Attaquant') or (detailJoueur.text=='Gardien') or (detailJoueur.text=='Défenseur') or (detailJoueur.text=='Milieu') or (detailJoueur.text=='Défenseur'):
            posteJoueur=detailJoueur.text

    #age du joueur
    if len(detailsJoueur[1])!=1:
        if detailsJoueur[1].text[3:6]=='ans': 
            dobJoueur=detailsJoueur[1].text 
        elif detailsJoueur[2].text[3:6]=='ans': 
            dobJoueur=detailsJoueur[2].text 
    elif detailsJoueur[2].text[3:6]=='ans': 
            dobJoueur=detailsJoueur[2].text 

    #si statistiques présentes
    if len(root.cssselect("td.gen a#lk_buts_1"))!=0:
        
        #nb de buts
        nbButs=root.cssselect("td.gen a#lk_buts_1")[0].text
    
        #nb buts encaissés pour gardien
        if(len(root.cssselect("td.gen a#lk_encaisses_1")))>0:
            nbButsEncaisses=root.cssselect("td.gen a#lk_encaisses_1")[0].text
        else:
            nbButsEncaisses=0

        #passes decisives
        nbPasses=root.cssselect("td.gen a#lk_passes_1")[0].text
        
        #temps de jeu
        tempsJeu=root.cssselect("td.gen a#lk_temps_1")[1].text
    
        #cartons jaunes
        cartonsJaunes=root.cssselect("td.gen a#lk_cartons_1")[0].text
    
        #cartons Rouges
        cartonsRouges=root.cssselect("td.gen a#lk_cartons_2")[0].text
    
        #fautes commises
        fautesCommises=root.cssselect("td.gen a#lk_detail_5")[0].text
    
        #fautes commises
        fautesSubies=root.cssselect("td.gen a#lk_detail_6")[0].text

    else:
        nbButs=0
        nbPasses=0
        tempsJeu=0
        cartonsJaunes=0
        cartonsRouges=0
        fautesCommises=0
        fautesSubies=0
    
    #retraite poste joueur pour les défenseurs
    if posteJoueur=='':
        posteJoueur='Defenseur'
    
    #calcule des points
    nbPointsJoueurGardien=float(tempsJeu)/90-float(nbButsContreEquipe)/2+float(nbPointsEquipe)*0.1
    nbPointsJoueurDefenseur=float(tempsJeu)/90-float(cartonsJaunes) -2*float(cartonsRouges) - float(nbButsContreEquipe)*0.25 +float(nbPointsEquipe)*0.1
    nbPointsJoueurMilieuDef=float(tempsJeu)/90-2*float(cartonsJaunes) -4*float(cartonsRouges) +float(nbPointsEquipe)*0.1
    nbPointsJoueurMilieuOff= float(nbPasses) + float(nbButs)*0.5 +float(nbPointsEquipe)*0.1
    nbPointsJoueurAttaquant=float(nbPasses)*0.5 + float(nbButs) +float(nbPointsEquipe)*0.1

    #enregistrement des resultats
    record = {}
    
    record["numJournee"]=numJournee
    record["equipe"]=teamName
    record["nomJoueur"]= nomJoueur
    record["nbButs"]= nbButs
    record["nbPasses"]= nbPasses      
    record["tempsJeu"]= tempsJeu 
    record["cartonsJaunes"]= cartonsJaunes 
    record["cartonsRouges"]= cartonsRouges
    record["fautesCommises"]= fautesCommises
    record["fautesSubies"]= fautesSubies
    record["posteJoueur"]=posteJoueur
    record["nbButsEncaissesGardien"]=nbButsEncaisses
    record["nbPointsEquie"]=nbPointsEquipe
    record["nbButsPourEquipe"]=nbButsPourEquipe
    record["nbButsContreEquipe"]=nbButsContreEquipe
    record["nbPointsJoueurGardien"]=nbPointsJoueurGardien
    record["nbPointsJoueurDefenseur"]=nbPointsJoueurDefenseur
    record["nbPointsJoueurMilieuDef"]=nbPointsJoueurMilieuDef
    record["nbPointsJoueurMilieuOff"]=nbPointsJoueurMilieuOff
    record["nbPointsJoueurAttaquant"]=nbPointsJoueurAttaquant
    record["lastUpdate"]=date.today()  
    record["dobJoueur"]=dobJoueur

    #save in datastore
    scraperwiki.sqlite.save(["numJournee", "equipe", "nomJoueur"], record)

#start
surlBase="http://www.lfp.fr/ligue1/classement?cat=Gen"

html = scraperwiki.scrape(surlBase)
rootClub = lxml.html.fromstring(html)

#recupère les lien vers tous les clubs
aClubs=rootClub.cssselect("div#liste_classement tr")

#boucle sur tous les clubs
for club in aClubs:

    if len(club.cssselect("td.club a")) !=0:

        teamName=club.cssselect("td.club a")[0].attrib['href'].replace('/club/','')
    
        nbPointsEquipe=club.cssselect("td.points")[0].text
        nbButsPourEquipe=club.cssselect("td.chiffres")[4].text
        nbButsContreEquipe=club.cssselect("td.chiffres")[5].text
        numJournee=club.cssselect("td.chiffres")[0].text

        print teamName

        html = scraperwiki.scrape("http://www.lfp.fr" + club.cssselect("td.club a")[0].attrib['href'])
        rootClub = lxml.html.fromstring(html)
    
        #liste de l'ensemble des joueurs d'un club
        aJoueur=rootClub.cssselect("a.lien_fiche")
    
        #boucle sur tous les joueurs
        for joueur in aJoueur:
            #lienJoueur=rootClub.cssselect("a.lien_fiche")
            html = scraperwiki.scrape("http://www.lfp.fr" + joueur.attrib['href'])
            root = lxml.html.fromstring(html)
        
            scrapeTable(root)   

