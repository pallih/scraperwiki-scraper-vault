import re
import scraperwiki
html = scraperwiki.scrape('http://www.setgame.com/puzzle/set.htm')
print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

for tr in soup.findAll('tr'):
    tds = tr.findAll("td");
    if len(tds) == 4:
         for td in tds:
             if td.findAll("a") and td.findAll("img"):
                 href = td.findAll("a")[0]['href']                                # javascript:board.cardClicked(12)
                 src  = td.findAll("img")[0]['src']                               # ../images/setcards/small/70.gif
                 if href.find("cardClicked") >= 0:
                     #print href + " " + src
                     position = re.sub("\).*$","",re.sub("^[^(]*\(","",href))     # 12
                     card     = "http://www.setgame.com/" + re.sub("^...","",src) # http://www.setgame.com/images/setcards/small/70.gif
                     id       = re.sub("\..*$","",re.sub("^.*/","",src))          # 70
                     #print position + " " + card + " " + id
                     record = { "Javascript" : href, "Card Position" : position, "src" : src, "Card Image URL" : card , "Card Identifier" : id}
                     scraperwiki.datastore.save(["Javascript","Card Position","src","Card Image URL","Card Identifier"], record)
import re
import scraperwiki
html = scraperwiki.scrape('http://www.setgame.com/puzzle/set.htm')
print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

for tr in soup.findAll('tr'):
    tds = tr.findAll("td");
    if len(tds) == 4:
         for td in tds:
             if td.findAll("a") and td.findAll("img"):
                 href = td.findAll("a")[0]['href']                                # javascript:board.cardClicked(12)
                 src  = td.findAll("img")[0]['src']                               # ../images/setcards/small/70.gif
                 if href.find("cardClicked") >= 0:
                     #print href + " " + src
                     position = re.sub("\).*$","",re.sub("^[^(]*\(","",href))     # 12
                     card     = "http://www.setgame.com/" + re.sub("^...","",src) # http://www.setgame.com/images/setcards/small/70.gif
                     id       = re.sub("\..*$","",re.sub("^.*/","",src))          # 70
                     #print position + " " + card + " " + id
                     record = { "Javascript" : href, "Card Position" : position, "src" : src, "Card Image URL" : card , "Card Identifier" : id}
                     scraperwiki.datastore.save(["Javascript","Card Position","src","Card Image URL","Card Identifier"], record)
