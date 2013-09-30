import httplib2
import urllib
import scraperwiki

# Test des deux libraries
import lxml.html
from BeautifulSoup import BeautifulSoup

'''
PROBLEME: 
* avec $ curl -d "list_id_produit=72009%2C90346%2C72008%2C72007&page=1&nb_par_page=100" http://www.jeuxvideo.fr/include/ajax/shopper.php?ajax=avis_jeux
j'ai 34 avis, ce qui correspond à ce qui est écrit sur le site
* avec httplib2 j'en obtiens 22

'''

# Definit les paramètres de connexion pour le jeu sur jeuxvideos.fr
def setConParam(url, body, header):
    request = {'url' : url, 'body' : body, 'header' : header}
    return request

# Scrape les donnees du jeu sur jeuxvideos.fr
def scraperJeuxVideos(myRequest):
    h = httplib2.Http()
    myUrl = myRequest['url']
    myBody = myRequest['body']
    myHeader = myRequest['header']
    resp, content = h.request(myUrl,"POST",headers=myHeader, body=urllib.urlencode(myBody))
    

    root = lxml.html.fromstring(content)
    avisList = root.cssselect(".avis-item")
    auteursListe = []
    datesListe = []
    commentaireListe = []
    notesListe = []

    #print content
    #print root.text_content() # 22! il y a un probleme!
    print len(avisList)
    
    for avis in avisList:
        if avis.find_class("sortie"):
            auteursListe.append(avis.cssselect(".by")[0].text_content())
            datesListe.append(avis.cssselect(".sortie")[0].text_content())
            commentaireListe.append(avis.cssselect(".content")[0].text_content())
            notesListe.append(avis.cssselect(".mark")[0].text_content())
 
    data ={}
    #scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`ID sujet` integer, `Auteur` text, `Note` text, `Date` text)")
    for i in range(len(notesListe)):
        data['ID sujet'] = i
        data['Note'] = notesListe[i]
        data['Date'] = datesListe[i]
        data['Auteur'] = auteursListe[i]
        scraperwiki.sqlite.save(['ID sujet'], data)

# Workflow pour jeuxvideos.fr
requestSonicHeroes = setConParam(
"http://www.jeuxvideo.fr/include/ajax/shopper.php?ajax=avis_jeux",
{'list_id_produit': '72009%2C72007%2C90346%2C72008', 'nb_par_page': '100', 'page':'1'},
{'Content-type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
)

scraperJeuxVideos(requestSonicHeroes)
import httplib2
import urllib
import scraperwiki

# Test des deux libraries
import lxml.html
from BeautifulSoup import BeautifulSoup

'''
PROBLEME: 
* avec $ curl -d "list_id_produit=72009%2C90346%2C72008%2C72007&page=1&nb_par_page=100" http://www.jeuxvideo.fr/include/ajax/shopper.php?ajax=avis_jeux
j'ai 34 avis, ce qui correspond à ce qui est écrit sur le site
* avec httplib2 j'en obtiens 22

'''

# Definit les paramètres de connexion pour le jeu sur jeuxvideos.fr
def setConParam(url, body, header):
    request = {'url' : url, 'body' : body, 'header' : header}
    return request

# Scrape les donnees du jeu sur jeuxvideos.fr
def scraperJeuxVideos(myRequest):
    h = httplib2.Http()
    myUrl = myRequest['url']
    myBody = myRequest['body']
    myHeader = myRequest['header']
    resp, content = h.request(myUrl,"POST",headers=myHeader, body=urllib.urlencode(myBody))
    

    root = lxml.html.fromstring(content)
    avisList = root.cssselect(".avis-item")
    auteursListe = []
    datesListe = []
    commentaireListe = []
    notesListe = []

    #print content
    #print root.text_content() # 22! il y a un probleme!
    print len(avisList)
    
    for avis in avisList:
        if avis.find_class("sortie"):
            auteursListe.append(avis.cssselect(".by")[0].text_content())
            datesListe.append(avis.cssselect(".sortie")[0].text_content())
            commentaireListe.append(avis.cssselect(".content")[0].text_content())
            notesListe.append(avis.cssselect(".mark")[0].text_content())
 
    data ={}
    #scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`ID sujet` integer, `Auteur` text, `Note` text, `Date` text)")
    for i in range(len(notesListe)):
        data['ID sujet'] = i
        data['Note'] = notesListe[i]
        data['Date'] = datesListe[i]
        data['Auteur'] = auteursListe[i]
        scraperwiki.sqlite.save(['ID sujet'], data)

# Workflow pour jeuxvideos.fr
requestSonicHeroes = setConParam(
"http://www.jeuxvideo.fr/include/ajax/shopper.php?ajax=avis_jeux",
{'list_id_produit': '72009%2C72007%2C90346%2C72008', 'nb_par_page': '100', 'page':'1'},
{'Content-type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
)

scraperJeuxVideos(requestSonicHeroes)
