# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string


lastrec = 7150
i =7143

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.artigianoinfiera.it/ita/dettaglio_espositori.php?ide=10696&id=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        #print soup
        id_smau=i
        i=i+1
        j=0
        k=0
        l=0
        print id_smau
        for dato_smau in soup.findAll('td'):
            x = str(dato_smau)
            j=j+1
            if j==6:
                citta = str(dato_smau.string)
                #print citta
            elif j==10:
                tel = str(dato_smau.string)
                #print tel
            elif j==18:
                prod = str(dato_smau.string)
                #print prod
        for dato_smau2 in soup.findAll('a'):
            y = str(dato_smau2)
            k=k+1
            if k==18:
                email = str(dato_smau2.string)
                #print email
        for dato_smau3 in soup.findAll('h2'):
            z = str(dato_smau3)
            l=l+1
            if l==3:
                nome = str(dato_smau3.string)
                #print nome
        scraperwiki.sqlite.save(unique_keys=["Progressivo"], data = {"Progressivo":id_smau, "Nome":nome, "Tel":tel, "Email":email, "Città":citta, "Prodotto":prod})

    except:
        #i=i+1
        continue




