import scraperwiki
import lxml.html
import datetime


now = datetime.datetime.now()

#check date and create URL

day_search = "http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=" + "%d" % now.day
month_search = "%2F" + "%d" % now.month
year_search = "%2F20"+ "%d" % now.year
end_search = "&enviaBusca=Buscar"

test_url = scraperwiki.scrape('http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=12%2F11%2F2012&enviaBusca=Buscar')
#url_ok = day_search + month_search + year_search + end_search

#print url_ok
#print "%d" % now.day
#print "%d" % now.month
#print "%d" % now.year


#scrape Data
  
root = lxml.html.fromstring(test_url) 
#root = lxml.html.fromstring(url_ok) 

conteudo = root.cssselect('div.fundo_ponto_escuro .ponto-de-alagamento') 
dia= now.strftime("%Y-%m-%d")
id = 0

#looking for all itens

#data_alaga = []

    
for div in conteudo:
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




