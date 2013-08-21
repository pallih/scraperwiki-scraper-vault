import scraperwiki
import lxml.html           
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil
from geopy import geocoders

#converte acentuacao em unescape para unicode: http://scraperwiki.com/scrapers/tramitacao-cldf/edit/
import copy, re
hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
hexentityMassage = [(re.compile('&#x([^;]+);'), 
    lambda m: '&#%d' % int(m.group(1), 16))]
def convert(html):
    return BeautifulSoup(html,
        convertEntities=BeautifulSoup.HTML_ENTITIES,
        markupMassage=hexentityMassage)

KEY = "ABQIAAAAyfn6gBmxwpyQxtGGaRkVLRS8-UheS-9Mv04KIr8hplvk5vm4LxS4PcgQhGbscOKXiJYc3mjdbgu0jg"
g = geocoders.Google(KEY)

SCRAP = True
#data = "28/05/2011"
#html = scraperwiki.scrape("http://www.queb.com.br/agenda.php?tp=6&dt="+data)
#print html

#soup = BeautifulSoup.BeautifulSoup(html)
#divs = soup.findAll('div', {"class" : "tbgal01", "style" : "padding-left:20px"})
#for div in divs:
    #print div

# create date objects
year = 2011
begin_year = datetime.date(year, 1, 1)
end_year = datetime.date(year, 12, 31)
one_day = datetime.timedelta(days=1)

next_day = begin_year
id = 0
for day in range(0, 366):
    if next_day > end_year:
        break
    d = next_day
#    print d, type(d)

    ultima_data = scraperwiki.sqlite.get_var("ultima_data")
    if not ultima_data:
        ultima_data = datetime.date(year, 2, 8)
    else:
        t = ultima_data.split('-')
        ultima_data = datetime.date(int(t[0]), int(t[1]), int(t[2]))

    # increment date object by one day
    next_day += one_day

    if d < ultima_data:
        continue

    if SCRAP:
        ds = str(d)
        html = scraperwiki.scrape("http://www.obaoba.com.br/porto-alegre/agenda?data="+ds)
        #print html
        #<div class="title-agenda">Balada | <a href="/porto-alegre/agenda/suite-angels-1?dia=28/05/2011">Suite Angels</a> | <a href="/porto-alegre/casa-de-show/petropolis/cafe-de-la-musique-poa">Cafe de La Musique - POA</a> </div>
        #soup = BeautifulSoup.BeautifulSoup(html)
        soup = convert(html)
        divs = soup.findAll('div', {"class" : "title-agenda"})
        for div in divs:
            #print div
            tipo = div.contents[0].split(" ")[0]
            A = div.findAll('a')
            if len(A) > 0:
                festa = A[0].contents[0]
                local = A[1].contents[0]

                endereco = local +" ,Porto Alegre, Rio Grande do Sul, Brasil"
                lat = None
                lng = None
                endereco = endereco.encode('utf-8')
                #print endereco
                try:
                    place, (lat, lng) = g.geocode(endereco)
                except:
                    pass # faz nada se deu erro

                print id, ds, local, festa, tipo, lat, lng
                scraperwiki.sqlite.save(unique_keys=["data","local"], data={"id":id, "data":ds, "local":local, "festa":festa, "latitude":lat, "longitude":lng})
                scraperwiki.sqlite.save_var("ultima_data", d)
                id += 1
