import scraperwiki
import sys
from bs4 import BeautifulSoup

#the url - CGE

#search_url = "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=08%2F11%2F2012&enviaBusca=Buscar"

day_search = "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="

month_search = "%2F"

year_search = "%2F20"

end_search = "&enviaBusca=Buscar"



#iterate over page numbers

for d in range(2,32):
    if d in range(1,10):
        d = "0" + str(d)
        search_url1 = day_search + str(d)
    else: 
        d = str(d)
        search_url1 = day_search + str(d)


    for m in range(1,13):
        if m in range(1,10):
            m = "0" + str(m)
            search_url2 = search_url1 + month_search + str(m)
        else: 
            m = str(m)
            search_url2 = search_url1 + month_search + str(m)


        for y in range(11,13):
                search_url = search_url2 + year_search + str(y) + end_search

                dia = "20"+str(y)+"-"+str(m)+"-"+str(d)
                
                print dia
                print search_url


                html = scraperwiki.scrape(search_url)


                #extract html
                soup = BeautifulSoup(html)
                #print soup
                    
                
                
                #bairro = soup.find_all("td.bairro")
                #zona = soup.find_all("h1.tit-bairros")
                alaga = soup.find_all("div.fundo_ponto_escuro .ponto-de-alagamento")
                
                #conteudo = soup.get_text("div.fundo_ponto_escuro .ponto-de-alagamento")   
                print alaga
                
                #for h1 in zona:
                #    print h1.text_content()
                
                
                #for td in bairro:
                #    print td.text_content()
                
                
                #for div in alaga:
                
                
                
                data = {"alagamento":alaga,
                            "datas":dia}
                


#    for results in data:
            # save records to the datastore
 #           scraperwiki.sqlite.save(["datas"],data=results)
#except:
#     print "falhou!"

import scraperwiki
import sys
from bs4 import BeautifulSoup

#the url - CGE

#search_url = "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=08%2F11%2F2012&enviaBusca=Buscar"

day_search = "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="

month_search = "%2F"

year_search = "%2F20"

end_search = "&enviaBusca=Buscar"



#iterate over page numbers

for d in range(2,32):
    if d in range(1,10):
        d = "0" + str(d)
        search_url1 = day_search + str(d)
    else: 
        d = str(d)
        search_url1 = day_search + str(d)


    for m in range(1,13):
        if m in range(1,10):
            m = "0" + str(m)
            search_url2 = search_url1 + month_search + str(m)
        else: 
            m = str(m)
            search_url2 = search_url1 + month_search + str(m)


        for y in range(11,13):
                search_url = search_url2 + year_search + str(y) + end_search

                dia = "20"+str(y)+"-"+str(m)+"-"+str(d)
                
                print dia
                print search_url


                html = scraperwiki.scrape(search_url)


                #extract html
                soup = BeautifulSoup(html)
                #print soup
                    
                
                
                #bairro = soup.find_all("td.bairro")
                #zona = soup.find_all("h1.tit-bairros")
                alaga = soup.find_all("div.fundo_ponto_escuro .ponto-de-alagamento")
                
                #conteudo = soup.get_text("div.fundo_ponto_escuro .ponto-de-alagamento")   
                print alaga
                
                #for h1 in zona:
                #    print h1.text_content()
                
                
                #for td in bairro:
                #    print td.text_content()
                
                
                #for div in alaga:
                
                
                
                data = {"alagamento":alaga,
                            "datas":dia}
                


#    for results in data:
            # save records to the datastore
 #           scraperwiki.sqlite.save(["datas"],data=results)
#except:
#     print "falhou!"

