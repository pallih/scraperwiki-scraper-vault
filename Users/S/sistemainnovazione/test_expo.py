# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string


lastrec = 300000
i =112704

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_smau=i
        i=i+1
        j=0
        k=0
        l=0
        print id_smau
        for dato_smau in soup.findAll('td'):
            x = str(dato_smau)
            j=j+1
            if j==28:
                citta = str(dato_smau.string)
                #print citta
            elif j==32:
                tel = str(dato_smau.string)
                #print tel
            elif j==34:
                fax = str(dato_smau.string)
                #print fax
        for dato_smau2 in soup.findAll('a'):
            y = str(dato_smau2)
            k=k+1
            if k==44:
                fiera = str(dato_smau2.string)
                #print fiera
            elif k==47:
                email = str(dato_smau2.string)
                #print email
        for dato_smau3 in soup.findAll('b'):
            z = str(dato_smau3)
            l=l+1
            if l==9:
                nome = str(dato_smau3.string)
                #print nome
        scraperwiki.sqlite.save(unique_keys=["Progressivo"], data = {"Fiera":fiera, "Progressivo":id_smau, "Nome":nome, "Tel":tel, "Fax":fax,  "Email":email})

    except:
        i=i+1
        continue

# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string


lastrec = 300000
i =112704

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_smau=i
        i=i+1
        j=0
        k=0
        l=0
        print id_smau
        for dato_smau in soup.findAll('td'):
            x = str(dato_smau)
            j=j+1
            if j==28:
                citta = str(dato_smau.string)
                #print citta
            elif j==32:
                tel = str(dato_smau.string)
                #print tel
            elif j==34:
                fax = str(dato_smau.string)
                #print fax
        for dato_smau2 in soup.findAll('a'):
            y = str(dato_smau2)
            k=k+1
            if k==44:
                fiera = str(dato_smau2.string)
                #print fiera
            elif k==47:
                email = str(dato_smau2.string)
                #print email
        for dato_smau3 in soup.findAll('b'):
            z = str(dato_smau3)
            l=l+1
            if l==9:
                nome = str(dato_smau3.string)
                #print nome
        scraperwiki.sqlite.save(unique_keys=["Progressivo"], data = {"Fiera":fiera, "Progressivo":id_smau, "Nome":nome, "Tel":tel, "Fax":fax,  "Email":email})

    except:
        i=i+1
        continue

