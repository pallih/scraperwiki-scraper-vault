import scraperwiki
from BeautifulSoup import BeautifulSoup

INDEX_PAGE = "http://www.bundestag.de/bundestag/abgeordnete17/alphabet/index.html"

def get_members(index):
    html = scraperwiki.scrape(index)
    page = BeautifulSoup(html)
    for l in page.findAll("div", {"class":"linkIntern"}):
        p = l.text.split(",")
        link = l.find("a")["href"]
        data = get_data(link)
        data["firstname"] = p[1]
        data["lastname"] = p[0]
        data["party"] = p[2]
        scraperwiki.datastore.save(["firstname", "lastname"], data)

def get_data(link):
    data = {}
    html = scraperwiki.scrape("http://www.bundestag.de/bundestag/abgeordnete17/alphabet/"+link)
    page = BeautifulSoup(html)
    contact = page.find("div", {"class":"contentArea"})
    try:
        data["website"] = contact.findAll("p")[2].find("a",{"class":"linkExtern"})["href"]
    except:
        pass
    try:
        picture = page.find("div", {"class": "bildDivPortrait"}).find("img")
        data["picture"] = "http://www.bundestag.de/bundestag/abgeordnete17/"+picture["src"].strip("../")
    except:
        pass
    for div in page.findAll("div", {"class": "contextBox"}):
        head = div.find("h2")
        if head:
            if head.text[:3] == "Gew":
                try:
                    data["constituency"] = div.find("a")["title"]
                except:
                    data["constituency"] = div.find("strong").text
        
    return data



get_members(INDEX_PAGE)