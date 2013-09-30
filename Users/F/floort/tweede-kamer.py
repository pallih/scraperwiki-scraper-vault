import scraperwiki
from BeautifulSoup import BeautifulSoup


# The frameset for the menu are written in javascript
home = scraperwiki.scrape("http://www.parlement.com")
start = home.find("<FRAME NAME=\"f15\"") + 17
end = home.find(">", start)
menu_url = home[start:end].split()[0][5:-1]
menu_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+menu_url))
link = menu_page.findAll("area")[2]["href"]
tweedekamer_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+link))
links = tweedekamer_page.findAll("a")
link = filter(lambda l : l.string == "Huidige Tweede Kamer", links)[0]["href"]
huidige_tweedekamer_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+link))
parties = huidige_tweedekamer_page.findAll("table", {"class":"infow"})
for p in parties:
    party = p.find("a", {"class":"h1"}).string.split()[0]
    member_table = p.findNext("table")
    for member in member_table.findAll("tr"):
        m = member.findAll("a")[1]
        member_url = "http://www.parlement.com"+m["href"]
        member_name = m.string
        member_page = BeautifulSoup(scraperwiki.scrape(member_url))
        member_img = "http://www.parlement.com"+member_page.find("img")["src"]
        tmp_html = str(member_page)
        start = tmp_html.find("e-mailadres")+22
        if start == 21: #21 = -1 + 22
            member_email = None
        else:
            member_email = tmp_html[start:tmp_html.find("<", start)]
        scraperwiki.datastore.save(["profile"], {
            "name": member_name,
            "party": party,
            "profile": member_url,
            "img": member_img,
            "email": member_email,
        })


import scraperwiki
from BeautifulSoup import BeautifulSoup


# The frameset for the menu are written in javascript
home = scraperwiki.scrape("http://www.parlement.com")
start = home.find("<FRAME NAME=\"f15\"") + 17
end = home.find(">", start)
menu_url = home[start:end].split()[0][5:-1]
menu_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+menu_url))
link = menu_page.findAll("area")[2]["href"]
tweedekamer_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+link))
links = tweedekamer_page.findAll("a")
link = filter(lambda l : l.string == "Huidige Tweede Kamer", links)[0]["href"]
huidige_tweedekamer_page = BeautifulSoup(scraperwiki.scrape("http://www.parlement.com"+link))
parties = huidige_tweedekamer_page.findAll("table", {"class":"infow"})
for p in parties:
    party = p.find("a", {"class":"h1"}).string.split()[0]
    member_table = p.findNext("table")
    for member in member_table.findAll("tr"):
        m = member.findAll("a")[1]
        member_url = "http://www.parlement.com"+m["href"]
        member_name = m.string
        member_page = BeautifulSoup(scraperwiki.scrape(member_url))
        member_img = "http://www.parlement.com"+member_page.find("img")["src"]
        tmp_html = str(member_page)
        start = tmp_html.find("e-mailadres")+22
        if start == 21: #21 = -1 + 22
            member_email = None
        else:
            member_email = tmp_html[start:tmp_html.find("<", start)]
        scraperwiki.datastore.save(["profile"], {
            "name": member_name,
            "party": party,
            "profile": member_url,
            "img": member_img,
            "email": member_email,
        })


