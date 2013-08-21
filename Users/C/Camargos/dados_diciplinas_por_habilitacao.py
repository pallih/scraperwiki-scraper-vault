import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from operator import itemgetter, attrgetter
url = 'https://sistemas.usp.br/jupiterweb/jupCursoLista?codcg=3&tipo=N'
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
lista = soup.findAll("a", {"class" : "link_gray"})
ind=0
for iten in lista:
    print iten  
    if str(iten).split('"')[1].find("jupCursoLista?codcg=3&amp;tipo=V")!=-1:
        break
    #print iten
    url_hab = 'https://sistemas.usp.br/jupiterweb/'+str(iten).split('"')[1].replace("amp;","") #por algum motivo o python acrescenta a palavra amp
    html_hab = scraperwiki.scrape(url_hab)                                                  #pegando o html da página
    soup_hab = BeautifulSoup(html_hab)                                               #transformando num objeto do BeautifulSoup
    hab = soup_hab.findAll("td")                 #pega todos os td (que eh quase todas as linhas do codigo fonte
    temp_nome=""                                 #zera o temporario nome
    temp_ano=""                                  #zera o temporario ano
    numero=1                       
    obrigatoriedade=1
    ind=ind+1
    for mat in hab:
        dados={}
        nome = mat.find("a", {"class" : "link_gray"})  #se existir class linkgray nessa linha coloca em nome
        span = mat.find("span")                        #se existe span nessa linha coloca em span
        obrig = mat.find("b")                          #se existir tipo b nessa linha coloca em obrig
        if span:                                       #se existir span
            if span.text.find("odo Ideal")!= -1:       #se o span eh o que estavamos procurando
                if temp_ano != span.text:              #para impedir repeticoes q tavam acontecendo
                    i=0
                    numero = 0
                    while(1):                          #transforma o texto da forma 7ºperiodo Ideal em 7
                        try: 
                            numero = numero*10
                            numero = numero + int(span.text[i])
                            i=i+1     
                        except ValueError: 
                            numero = numero/10
                            break
                    temp_ano = span.text  
        if obrig:                                      #se existir obrig
            if obrig.text.find("Optativa")!=-1:
                if obrig.text.find("Eletiva")!=-1:
                    obrigatoriedade=2
                else:
                    obrigatoriedade=3
                
        if nome and temp_nome != str(nome.text):    #para impedir repeticoes q tavam acontecendo
            #print nome.text + ";" + str(numero) + ";" + str(iten).split('codcur=')[1].split('&')[0] + ";" + str(obrigatoriedade)
            dados['indice']=ind
            dados['nome']=nome.text
            dados['periodo']=numero
            dados['codcur']=str(iten).split('codcur=')[1].split('&')[0]
            dados['codhab']=str(iten).split('codhab=')[1].split('&')[0]
            dados['obri']=obrigatoriedade
            #print dados
            scraperwiki.sqlite.save(['indice','nome'],dados)       #salva os dados no scrapper       
            temp_nome = str(nome.text)

