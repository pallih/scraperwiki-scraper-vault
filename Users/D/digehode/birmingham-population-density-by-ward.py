import scraperwiki,re
from BeautifulSoup import BeautifulSoup
brum = scraperwiki.scrape("http://openlylocal.com/councils/167-Birmingham-City-Council")

def text2num(txt):
    return int("".join(txt.split(",")))

def get_ward_data(ward):
    html=scraperwiki.scrape(ward)
    wardpage=BeautifulSoup(html)
    coords= str(wardpage.find(text=re.compile("boundary_line_coords")))
    coords=coords[coords.find("[[[")+1:coords.find("]]]")+2]
    titletext=wardpage.find("title").text
    titletext=titletext[:titletext.find(":")-6]
    stats=wardpage.find("div",{"class":"stats_in_words"}).text
    dwellings=stats[:stats.find("dwellings")]
    people=stats.split(", ")[1]
    people=people[:people.find("people")]
    dwellings=text2num(dwellings)
    people=text2num(people)
    size=float(wardpage.find("dd",{"class":"size"}).text.split(" ")[0])
    #print "[%s]"%titletext,":",dwellings,":",people,":",size,":",coords
    data={"ward":titletext.upper(),"dwellings":dwellings,"people":people,"size(hectares)":size,"boundary":coords}
    scraperwiki.datastore.save(["ward"], data) 

soup = BeautifulSoup(brum)
wards = soup.findAll("a", { "class" : "ward_link" })
for ward in wards:
    get_ward_data("http://openlylocal.com"+ward['href'])
    
