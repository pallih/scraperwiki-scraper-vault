# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

#CREATE TABLE 'albo_milano' ('Codice Fiscale' text, 'Progressivo' integer, 'Cognome' text, 'Nome' text, 'Email' text, 'Tel' text, 'Fax' text, 'CAP' text, 'Indirizzo' text)

lastrec = 532
i = 268

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.ordineavvocativigevano.it/index.php?option=com_contact&view=contact&id=' + str(i)+'&directory=58')
        soup = BeautifulSoup.BeautifulSoup(html)
        #print soup
        #soup_pret = soup.prettify()
        #print soup.prettify()
        id_avv=i
        i=i+1
        j=0
        print id_avv
        for dato_avv in soup.findAll('div'):
            #print dato_avv
            x = str(dato_avv)
            j=j+1
            if j==27:
                cognome_nome = str(dato_avv.string)
                print cognome_nome
            elif j==29:
                indiriz = str(dato_avv.prettify())
                print indiriz
        #scraperwiki.sqlite.save(unique_keys=["Codice fiscale"], data = {"Codice fiscale":codfisc, "Tel":tel, "Email":email, "Cognome e nome":cognome_nome, "Indirizzo":indiriz, "Progressivo":id_avv})

    except:
        i=i+1
        continue
# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

#CREATE TABLE 'albo_milano' ('Codice Fiscale' text, 'Progressivo' integer, 'Cognome' text, 'Nome' text, 'Email' text, 'Tel' text, 'Fax' text, 'CAP' text, 'Indirizzo' text)

lastrec = 532
i = 268

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.ordineavvocativigevano.it/index.php?option=com_contact&view=contact&id=' + str(i)+'&directory=58')
        soup = BeautifulSoup.BeautifulSoup(html)
        #print soup
        #soup_pret = soup.prettify()
        #print soup.prettify()
        id_avv=i
        i=i+1
        j=0
        print id_avv
        for dato_avv in soup.findAll('div'):
            #print dato_avv
            x = str(dato_avv)
            j=j+1
            if j==27:
                cognome_nome = str(dato_avv.string)
                print cognome_nome
            elif j==29:
                indiriz = str(dato_avv.prettify())
                print indiriz
        #scraperwiki.sqlite.save(unique_keys=["Codice fiscale"], data = {"Codice fiscale":codfisc, "Tel":tel, "Email":email, "Cognome e nome":cognome_nome, "Indirizzo":indiriz, "Progressivo":id_avv})

    except:
        i=i+1
        continue
