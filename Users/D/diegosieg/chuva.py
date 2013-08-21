import scraperwiki
import lxml.html


#test_url = scraperwiki.scrape('http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=12%2F11%2F2012&enviaBusca=Buscar')


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
                
                

                #root = lxml.html.fromstring(test_url)
                root = lxml.html.fromstring(search_url) 
                #bairro = root.cssselect('td.bairro') 
                #zona = root.cssselect('h1.tit-bairros')
                alaga = root.cssselect('div.fundo_ponto_escuro .ponto-de-alagamento')
                
                print alaga
             
                #for td in bairro:
                #        data_bairro = td.text_content()
                        #print data_bairro
                                           
                #for h1 in zona:
                #       data_zona = td.text_content()
                #       print h1.text_content()
                        
                for div in alaga:
                        data_alaga = div.text_content()
                        print data_alaga
                        data={"dias":dia,
                             "alagamento":data_alaga
                             }
                        scraperwiki.sqlite.save(["dias"], data)
    
                    #for div in situ:
                    #    print li.text_content()          
                    
                    #if div is not defined:
                    #    pass
                    
                    #data = {"alagamento":div.text_content(),
                    #        "regiao":h1.text_content(),
                    #        "bairros":td.text_content()
                    #        }
                        
                        
                    #for results in data:
                       

