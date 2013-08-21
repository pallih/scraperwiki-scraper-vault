import scraperwiki 
import lxml.html 
from datetime import date

def savedata(page,c): #,id):
    data = {}
    i = 0
    k = 0
    table = page.cssselect("table")[8]
    for tr in table.cssselect('tr'):
        if i != 0:
            k += 1
            if k == 1:
                place = tr.cssselect('td')[0].text_content().strip()
                if place == '':
                    place = p
                else:
                    p = place
                kind = tr.cssselect('td')[1].text_content().strip()
                title = tr.cssselect('td')[2].text_content().strip().replace(',',' ')
            elif k == 2:
                when = tr.cssselect('td')[2].text_content().strip().split(" Al ")
                start = when[0][4:len(when[0])]
                end = when[1]
            elif k == 3:
                where = tr.cssselect('td')[2].text_content().strip().replace(',',' ')
                id = "%s_%s_%s_%s_%s_%s" % (title,place,kind,start,end,where)
                id = id.replace(" ","_") 
                data = {'id':id,'titolo':title,'luogo':place,'tipo':kind,'inizio':start,'fine':end,'dove':where,'conta':c}
                c +=1
                scraperwiki.sqlite.save(unique_keys=['id'], data=data) 
                k = 0   
        i += 1
    return c


year = str(date.today().year)
day = str(date.today().day)
month = str(date.today().month)
year = str(date.today().year)
if len(day) == 1:
    day = "0" + day
if len(month) == 1:
    month = "0" + month
today = day + "/" + month + "/" + year
totrecord = 0



firstyear = 1998
lastyear = int(year)+1
url = "http://www.trentinocultura.net/asp_cat/main.asp?IDProspettiva=35&SearchType=AGENDA_SEARCH&Pag=PAGINA&data=31/12/ANNO&TipoVista=AGENDA"
npage = 1
for y in range(int(firstyear),int(lastyear)):
    surl = url.replace('PAGINA',str(npage))
    surl = surl.replace('ANNO',str(y))
    html = scraperwiki.scrape(surl) 
    root = lxml.html.fromstring(html)
    table = root.cssselect("table")[4]
    tr = table.cssselect("tr")[0]
    tot= tr.cssselect('td')[4].text_content().strip().split("/")[1]
    for i in range(1,int(tot)):
        searchurl = url.replace('PAGINA',str(i))
        searchurl = searchurl.replace('ANNO',str(y))
        if i  >1:
            searchurl += '&IdSel=' + str(i-1)
        searchhtml = scraperwiki.scrape(searchurl)
        page = lxml.html.fromstring(searchhtml)
        totrecord = savedata(page,totrecord)

