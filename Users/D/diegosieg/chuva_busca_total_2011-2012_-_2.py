import scraperwiki
import lxml.html


#test_url = scraperwiki.scrape('http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=12%2F11%2F2012&enviaBusca=Buscar')


day_search = "scraperwiki.scrape('http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="

month_search = "%2F"

year_search = "%2F20"

end_search = "&enviaBusca=Buscar')"



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
                #for results in search_url:
                #root = lxml.html.fromstring(test_url)
                root = lxml.html.fromstring(search_url) 
                                                    
                alaga = root.cssselect('div.fundo_ponto_escuro .ponto-de-alagamento')
                id = 0
                                                   
                for div in alaga:
                    data_alaga = div.text_content()
                    print data_alaga
                    id = id + 1
                    if len(data_alaga)>0:
                       data = {
                            'ids' : id,
                            'dias' : dia,
                            'alagamentos' : div[0].text_content()
                                                    }
                       scraperwiki.sqlite.save(unique_keys=['ids'], data=data)
                                             
