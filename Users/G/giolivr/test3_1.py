# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

#CREATE TABLE 'albo_milano' ('Codice Fiscale' text, 'Progressivo' integer, 'Cognome' text, 'Nome' text, 'Email' text, 'Tel' text, 'Fax' text, 'CAP' text, 'Indirizzo' text)

lastrec = 40000
i = 33164

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.ordineavvocatimilano.it/ered/html/dettaglio_albo.asp?bott=ok&idvoce=4&id=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_avv=i
        i=i+1
        j=0
        print id_avv
        for dato_avv in soup.findAll('td'):
            x = str(dato_avv)
            j=j+1
            if j==4:
                tipo = str(dato_avv.string)
                print tipo
            elif j==7:
                cognome = str(dato_avv.string)
                #print cognome
            elif j==10:
                nome = str(dato_avv.string)
                #print nome
            elif j==19:
                codfisc = str(dato_avv.string)
                #print codfisc
            elif j==22:
                indiriz = str(dato_avv.string)
                #print indiriz
            elif j==25:
                citta = str(dato_avv.string)
                #print citta
            elif j==28:
                cap = str(dato_avv.string)
                #print cap
            elif j==31:
                tel = str(dato_avv.string)
                #print tel
            elif j==34:
                fax = str(dato_avv.string)
                #print fax
            elif j==37:
                email = str(dato_avv.string)
                #print email
        scraperwiki.sqlite.save(unique_keys=["Codice fiscale"], data = {"Codice fiscale":codfisc, "Tel":tel, "Fax":fax, "Email":email, "Nome":nome, "Cognome":cognome, "CAP":cap, "Indirizzo":indiriz, "Progressivo":id_avv, "Categoria":tipo})

    except:
        i=i+1
        continue
