import scraperwiki
import difflib
from BeautifulSoup import BeautifulSoup
baseurl = 'http://www.dati.gov.it'
step1 = '/ricerca_dataset'
page = '?page='
url = baseurl + step1
html = scraperwiki.scrape(url) 
print url
soup = BeautifulSoup(html)
s = soup.findAll(attrs={'class' : 'pager-last last'})[0].findAll("a")
np = str(s[0]).split('"')[3].split('?')[1].split('=')[1]
id = 0
for i in range(0,int(np)+1):
    url = baseurl + step1 + page + str(i)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    rows = soup.findAll(attrs={'class':'view-content'})[0].findAll("div")
    for r in rows:
        field = str(r['class'])
        if ( field.find('views-field views-field-title') > -1):
            scheda = str(r.contents[1].findAll('a')[0]).split('"')[1]
            urlscheda = baseurl + scheda
            html = scraperwiki.scrape(urlscheda)
            soupscheda = BeautifulSoup(html)
            rowsscheda = soupscheda.findAll(attrs={'id':'content'})[0].findAll("div")
            manager = ''
            period_from = ''
            period_to = ''
            license = 'no'
            sourceurl = ''
            description = ''
            urlmanager =  ''
            author = ''
            email = ''
            nation = ''
            region = ''
            province = ''
            lastupdate = ''
            city = ''
            for rs in rowsscheda:
                fieldscheda = str(rs['class'])
                if (fieldscheda.find('field-type-text-with-summary') > -1):
                    description = rs.findAll('p')[0].contents
                if (fieldscheda.find('field field-name-field-url-dataset field-type-text field-label-above')>-1):
                    sourceurl = rs.findAll('a')
                    sourceurl = sourceurl[0].contents[0]
                if (fieldscheda.find('field field-name-field-licenza field-type-taxonomy-term-reference field-label-above clearfix')>-1):
                    license = rs.findAll('li')[0].contents
                    print license
                if (fieldscheda == 'field field-name-field-data-load field-type-datetime field-label-above'):
                    lastupdate = rs.findAll('span')[0].contents[0]
                if (fieldscheda == 'field field-name-field-data-from-to field-type-datetime field-label-above'):
                    period = rs.findAll('span')
                    period_from = ''
                    period_to = ''
                    if (len(period) > 0):
                        if (len(period) == 1):
                            period_from = period[0].contents[0]
                        if (len(period) == 2):
                            period_from = period[0].contents[0]
                            period_to = period[1].contents[0]
                if (fieldscheda == 'field field-name-field-ente-gestore field-type-text field-label-above'):
                    manager = rs.findAll('field-label')
                    if len(manager):
                        manager = manager[0]
                    else:
                        manager = ""
                if (fieldscheda.find('field-name-field-site-url-ente field-type-text field-label-above')>1):
                    urlmanager = rs.findAll('a')[0].contents[0]
                if (fieldscheda == 'field field-name-field-nome-funz-uo field-type-text field-label-above'):
                    author = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-email-rif field-type-email field-label-above'):
                    email = rs.findAll('a')[0].contents[0]
                if (fieldscheda == 'field field-name-field-nazione field-type-text field-label-above'):
                    nation = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-regione field-type-list-text field-label-above'):
                    region = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-provincia field-type-list-text field-label-above'):
                    province = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-comune field-type-list-text field-lable-above'):
                    city = rs.findAll('div')[2].contens[0]
            title = scheda.replace("content/","")
            title = title.replace("-"," ")
            title = title.replace("/","")
            r = difflib.SequenceMatcher(None, manager, region).ratio()
            if (r > 0.7):
                title = title + " - " + manager
            else:
                title = title + " - " + manager + " " + region
            data = {
                'id' : baseurl + scheda,
                'title': title,
                'manager' : manager,
                'description': description,
                'lastupdate' : lastupdate,
                'period_from' : period_from,
                'period_to': period_to,
                'license' : license,
                'sourceurl' : sourceurl,
                'urlmanager' : urlmanager,
                'author' : author,
                'email' : email,
                'nation' : nation,
                'region' : region,
                'province': province,
                'city': city
            }
            id += 1
            #print "%s %s%s" % (id,baseurl,scheda)
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)



import scraperwiki
import difflib
from BeautifulSoup import BeautifulSoup
baseurl = 'http://www.dati.gov.it'
step1 = '/ricerca_dataset'
page = '?page='
url = baseurl + step1
html = scraperwiki.scrape(url) 
print url
soup = BeautifulSoup(html)
s = soup.findAll(attrs={'class' : 'pager-last last'})[0].findAll("a")
np = str(s[0]).split('"')[3].split('?')[1].split('=')[1]
id = 0
for i in range(0,int(np)+1):
    url = baseurl + step1 + page + str(i)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    rows = soup.findAll(attrs={'class':'view-content'})[0].findAll("div")
    for r in rows:
        field = str(r['class'])
        if ( field.find('views-field views-field-title') > -1):
            scheda = str(r.contents[1].findAll('a')[0]).split('"')[1]
            urlscheda = baseurl + scheda
            html = scraperwiki.scrape(urlscheda)
            soupscheda = BeautifulSoup(html)
            rowsscheda = soupscheda.findAll(attrs={'id':'content'})[0].findAll("div")
            manager = ''
            period_from = ''
            period_to = ''
            license = 'no'
            sourceurl = ''
            description = ''
            urlmanager =  ''
            author = ''
            email = ''
            nation = ''
            region = ''
            province = ''
            lastupdate = ''
            city = ''
            for rs in rowsscheda:
                fieldscheda = str(rs['class'])
                if (fieldscheda.find('field-type-text-with-summary') > -1):
                    description = rs.findAll('p')[0].contents
                if (fieldscheda.find('field field-name-field-url-dataset field-type-text field-label-above')>-1):
                    sourceurl = rs.findAll('a')
                    sourceurl = sourceurl[0].contents[0]
                if (fieldscheda.find('field field-name-field-licenza field-type-taxonomy-term-reference field-label-above clearfix')>-1):
                    license = rs.findAll('li')[0].contents
                    print license
                if (fieldscheda == 'field field-name-field-data-load field-type-datetime field-label-above'):
                    lastupdate = rs.findAll('span')[0].contents[0]
                if (fieldscheda == 'field field-name-field-data-from-to field-type-datetime field-label-above'):
                    period = rs.findAll('span')
                    period_from = ''
                    period_to = ''
                    if (len(period) > 0):
                        if (len(period) == 1):
                            period_from = period[0].contents[0]
                        if (len(period) == 2):
                            period_from = period[0].contents[0]
                            period_to = period[1].contents[0]
                if (fieldscheda == 'field field-name-field-ente-gestore field-type-text field-label-above'):
                    manager = rs.findAll('field-label')
                    if len(manager):
                        manager = manager[0]
                    else:
                        manager = ""
                if (fieldscheda.find('field-name-field-site-url-ente field-type-text field-label-above')>1):
                    urlmanager = rs.findAll('a')[0].contents[0]
                if (fieldscheda == 'field field-name-field-nome-funz-uo field-type-text field-label-above'):
                    author = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-email-rif field-type-email field-label-above'):
                    email = rs.findAll('a')[0].contents[0]
                if (fieldscheda == 'field field-name-field-nazione field-type-text field-label-above'):
                    nation = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-regione field-type-list-text field-label-above'):
                    region = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-provincia field-type-list-text field-label-above'):
                    province = rs.findAll('div')[2].contents[0]
                if (fieldscheda == 'field field-name-field-comune field-type-list-text field-lable-above'):
                    city = rs.findAll('div')[2].contens[0]
            title = scheda.replace("content/","")
            title = title.replace("-"," ")
            title = title.replace("/","")
            r = difflib.SequenceMatcher(None, manager, region).ratio()
            if (r > 0.7):
                title = title + " - " + manager
            else:
                title = title + " - " + manager + " " + region
            data = {
                'id' : baseurl + scheda,
                'title': title,
                'manager' : manager,
                'description': description,
                'lastupdate' : lastupdate,
                'period_from' : period_from,
                'period_to': period_to,
                'license' : license,
                'sourceurl' : sourceurl,
                'urlmanager' : urlmanager,
                'author' : author,
                'email' : email,
                'nation' : nation,
                'region' : region,
                'province': province,
                'city': city
            }
            id += 1
            #print "%s %s%s" % (id,baseurl,scheda)
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)



