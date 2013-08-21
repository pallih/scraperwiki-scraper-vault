import scraperwiki
import lxml.html
import BeautifulSoup
from BeautifulSoup import BeautifulSoup

def cerca(html,search,nrline,offset):
    i=html.find(search)
    #print "I " + str(i)
    if i > 0:
        i=i+len(search)
        j=i+offset
        #esegue split ed elimina tutto quello che inizia con <
        s = html[i:j]
        s = s.splitlines(nrline)
        #print "S " + str(s)
        rs = s[nrline]
        rs = rs.strip ("\r")
        rs = rs.strip ("\n")
        return (rs)
    else:
        return ''

pagine = range(1,97)

for count in pagine:
    try:
        searchURL = "http://www.comuni-italiani.it/cap/%02d.html"%count
        print searchURL 
        html = scraperwiki.scrape(searchURL)
        html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
        tables = html.findAll('table')

    except:
        print "error for WKI_ID:"+ str(id)
    
    rows = tables[5].findAll('tr')
    li = {}
    
    for row in rows:
        try:
            cells = row.findChildren('td')
            if len(cells) <= 4:
                li['CAP'] = cells[0].text
                li['COMUNE'] = cells[1].text
                #print cells
                #print cells[1]
                #print str(cells[1])[27:40]
                comune =  str(cells[1])[31:39]
                comuneUrl = "http://www.comuni-italiani.it/" + comune
                #print comuneUrl

                html = scraperwiki.scrape(comuneUrl)
                #print html
                print cerca (html,'../../tel/',0,10)
                #html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
                #Trovare il modo di recuperare il prefisso del comune e altri dati                

                #match = re.search(r'href=?+)', str(cells[1]))
                #if match:
                #    print match.group(0)


                scraperwiki.sqlite.save(unique_keys=['CAP','COMUNE'], data=li)                    
        except:
            print "error for WKI_ID:"+ str(id)
