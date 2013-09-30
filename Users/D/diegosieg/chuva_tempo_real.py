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
url_ok = day_search + month_search + year_search + end_search

#print url_ok
#print "%d" % now.day
#print "%d" % now.month
#print "%d" % now.year


#scrape Data
  
root = lxml.html.fromstring(test_url) 
#root = lxml.html.fromstring(url_ok) 

bairro = root.cssselect('td.bairro') 
zona = root.cssselect('h1.tit-bairros')
alaga = root.cssselect('div.ponto-de-alagamento')
dia= now.strftime("%Y-%m-%d")

#looking for all itens

data_bairro = []
data_zona = []
data_alaga = []

for h1 in zona:
    #print h1.text_content()
    #data_zona = h1.text_content()
    data_temp = h1.text_content()
    for dt_z in data_temp:
        data_zona.append(data_temp)

print data_zona
        
    

for td in bairro:
    #print td.text_content() 
    #data_bairro = td.text_content()
    data_temp2 = td.text_content()
    for dt_b in data_temp2:
        data_bairro.append(data_temp2)

print data_bairro
    
       
for div in alaga:
    #print div.text_content() 
    #data_alaga = div.text_content()
    data_temp3 = div.text_content()
    for dt_a in data_temp3:
        data_alaga.append(data_temp3)

print data_alaga
    




#save data on datastorage


#print data_zona
#print data_bairro
#print data_alaga

#data = {}

#for results in data_zona, data_bairro, data_alaga:
data = [{"dias":dia, 
            "bairros":data_bairro,
            "zona":data_zona,
            "alagamentos":data_alaga
            }]

scraperwiki.sqlite.save(["dias"], data)


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
url_ok = day_search + month_search + year_search + end_search

#print url_ok
#print "%d" % now.day
#print "%d" % now.month
#print "%d" % now.year


#scrape Data
  
root = lxml.html.fromstring(test_url) 
#root = lxml.html.fromstring(url_ok) 

bairro = root.cssselect('td.bairro') 
zona = root.cssselect('h1.tit-bairros')
alaga = root.cssselect('div.ponto-de-alagamento')
dia= now.strftime("%Y-%m-%d")

#looking for all itens

data_bairro = []
data_zona = []
data_alaga = []

for h1 in zona:
    #print h1.text_content()
    #data_zona = h1.text_content()
    data_temp = h1.text_content()
    for dt_z in data_temp:
        data_zona.append(data_temp)

print data_zona
        
    

for td in bairro:
    #print td.text_content() 
    #data_bairro = td.text_content()
    data_temp2 = td.text_content()
    for dt_b in data_temp2:
        data_bairro.append(data_temp2)

print data_bairro
    
       
for div in alaga:
    #print div.text_content() 
    #data_alaga = div.text_content()
    data_temp3 = div.text_content()
    for dt_a in data_temp3:
        data_alaga.append(data_temp3)

print data_alaga
    




#save data on datastorage


#print data_zona
#print data_bairro
#print data_alaga

#data = {}

#for results in data_zona, data_bairro, data_alaga:
data = [{"dias":dia, 
            "bairros":data_bairro,
            "zona":data_zona,
            "alagamentos":data_alaga
            }]

scraperwiki.sqlite.save(["dias"], data)


