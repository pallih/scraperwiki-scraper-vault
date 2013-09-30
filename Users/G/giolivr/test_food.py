# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

lastrec = 10000
i = 99096

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_expo=i
        print id_expo
        id_str = str(id_expo) 
        i=i+1
        j=0
        k=0
        l=0
#        for dato_expo in soup.findAll('td'):
#            x = str(dato_expo)
#            j=j+1
#            if j==28:
#                citta = str(dato_expo.string)
#                print citta
#            elif j==32:
#                tel = str(dato_expo.string)
#                print tel
#            elif j==34:
#                fax = str(dato_expo.string)
#                print fax
#        record1 = {"ID":id_str, "Città":citta, "Telefono":tel, "Fax":fax}
#        scraperwiki.sqlite.save(["ID"], record1)
        for dato_expo in soup.findAll('a'):
            x = str(dato_expo)
            k=k+1
            if k==38:
                fiera = str(dato_expo.string)
                print fiera
            elif k==45:
                email = str(dato_expo.string)
                print email
            elif k==46:
                website = str(dato_expo.string)
                print website
        record2 = {"ID":id_str, "Fiera":fiera, "Email":email, "Website":website}
        scraperwiki.sqlite.save(["ID"], record2)
#        for dato_expo in soup.findAll('h1'):
#            x = str(dato_expo)
#            l=l+1
#            if l==4:
#                nome = str(dato_expo.string)
#                print nome
#        record3 = {"ID":id_str, "Nome":nome}
#        scraperwiki.sqlite.save(["ID"], record3)

    except:
        print i
        continue
# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

lastrec = 10000
i = 99096

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_expo=i
        print id_expo
        id_str = str(id_expo) 
        i=i+1
        j=0
        k=0
        l=0
#        for dato_expo in soup.findAll('td'):
#            x = str(dato_expo)
#            j=j+1
#            if j==28:
#                citta = str(dato_expo.string)
#                print citta
#            elif j==32:
#                tel = str(dato_expo.string)
#                print tel
#            elif j==34:
#                fax = str(dato_expo.string)
#                print fax
#        record1 = {"ID":id_str, "Città":citta, "Telefono":tel, "Fax":fax}
#        scraperwiki.sqlite.save(["ID"], record1)
        for dato_expo in soup.findAll('a'):
            x = str(dato_expo)
            k=k+1
            if k==38:
                fiera = str(dato_expo.string)
                print fiera
            elif k==45:
                email = str(dato_expo.string)
                print email
            elif k==46:
                website = str(dato_expo.string)
                print website
        record2 = {"ID":id_str, "Fiera":fiera, "Email":email, "Website":website}
        scraperwiki.sqlite.save(["ID"], record2)
#        for dato_expo in soup.findAll('h1'):
#            x = str(dato_expo)
#            l=l+1
#            if l==4:
#                nome = str(dato_expo.string)
#                print nome
#        record3 = {"ID":id_str, "Nome":nome}
#        scraperwiki.sqlite.save(["ID"], record3)

    except:
        print i
        continue
