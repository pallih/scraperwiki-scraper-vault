import scraperwiki
import BeautifulSoup 

#Scrap level in all reservoir Catalunya

url = "http://www.embalses.net/cuenca-11-c-i--cataluna.html"
html = scraperwiki.scrape(url)
soup = BeautifulSoup.BeautifulSoup(html)
reservoirs = soup.findAll("table",{"class":"TablaMenu"})[0].findAll("tr",{"class":"ResultadoCampo"})
date = soup.findAll("div",{"class":"Seccion"})[1].findAll("div",{"class":"Campo"})[0].getText()[-12:-2]
for d in reservoirs:
    t = d.findAll("td")
    name = t[0].getText() 
    capacity = t[1].getText()
    retain = t[2].getText()   
    variation= t[3].getText()
    id = date+"_"+name.replace(" ","_")
    data = {"id":id,"name":name,"capacity":capacity,"retain":retain,"variation":variation,"date-reading":date}
    scraperwiki.sqlite.save(unique_keys=['id'],data=data)

    



