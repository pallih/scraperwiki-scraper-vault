import scraperwiki         
import lxml.html

# create table with some number field types
sql="CREATE TABLE IF NOT EXISTS `mydata` (titolo text, `discipline` text, `ente` text, `data_end` date, `url` text, `crediti` real, `data_start` date, `professioni` text, `website_ente` text, `verifica` text, `comp_sistema` text, `sponsor` text, `obiettivo` text, `comp_processo` text, `durata` text, `comp_tecniche` text, `costo` real, `tipo_fad` text, `last_data` date, `localita` text)"
scraperwiki.sqlite.execute(sql)


# REFRESH ONLY
ONLYREFRESH=True

def text(s):
    try:
        s.split(':')
    finally:
        return s.split(':',1)[1]        
    
    return s

def implode(a, sep):

    aa=a[0].text_content().split(sep);   

    joined=','.join(aa) 

    return joined[1:]

def dateiso(d):
    tk=d.split('/')
    return tk[2]+'-'+tk[1]+'-'+tk[0]




url="http://www.fadecm.net/fad-ecm-2012?page=";

if(ONLYREFRESH):
    ultimo=8
else:
    html = scraperwiki.scrape("http://www.fadecm.net/fad-ecm-2012?page=0")
    root = lxml.html.fromstring(html)
    aa=root.cssselect(".pager-last a")
    ultimo= aa[0].attrib['href'].split('=')[1]


# print ultimo

ll=[]

for i in range(0,int(ultimo)):

    ll.append( url+str(i))

#print ll

plink=[]



for link in ll:
    dom=scraperwiki.scrape(link)
    root2 = lxml.html.fromstring(dom)
    h3s=root2.cssselect(".views-row0 h3 a")

    
    # tutti i link dei doc
    for h3 in h3s:
        plink.append(h3.attrib['href'])


# Secodna parte


print plink

for pp in plink:
    url2="http://www.fadecm.net" + str(pp)
    html2=scraperwiki.scrape(url2)
    root3 = lxml.html.fromstring(html2)
    data={
        'url' : url2, 
        'crediti' : (float(text(root3.cssselect(".field-field-crediti")[0].text_content()))) if root3.cssselect(".field-field-crediti") else None,
        'data_start' : (dateiso(root3.cssselect(".date-display-start")[0].text_content())) if root3.cssselect(".date-display-start") else '',
        'data_end' : (dateiso(root3.cssselect(".date-display-end")[0].text_content())) if root3.cssselect(".date-display-end") else '',
        'durata' : text(root3.cssselect(".field-field-durata")[0].text_content()),
        'costo' : float(text(root3.cssselect(".field-field-quota")[0].text_content()).replace("€".decode('utf8'), '').strip()),
        'sponsor' : (text(root3.cssselect(".field-field-sponsor")[0].text_content())) if root3.cssselect(".field-field-sponsor") else '',
        'verifica' : (text(root3.cssselect(".field-field-verifica")[0].text_content())) if root3.cssselect(".field-field-verifica") else '',
        'ente' : (text(root3.cssselect(".field-field-azienda")[0].text_content())) if root3.cssselect(".field-field-azienda") else '',
        'website_ente' : (text(root3.cssselect(".field-field-website")[0].text_content())) if root3.cssselect(".field-field-website") else '',
        'obiettivo' : (root3.cssselect(".field-field-obiettivo-formativo")[0].text_content()) if root3.cssselect(".field-field-obiettivo-formativo") else '',
        'tipo_fad' : (text(root3.cssselect(".field-field-tipologia-evento")[0].text_content())) if root3.cssselect(".field-field-tipologia-evento") else '',
        'comp_tecniche' : (text(root3.cssselect(".field-field-com-tecniche")[0].text_content())) if root3.cssselect(".field-field-com-tecniche") else '',
        'comp_processo' : (text(root3.cssselect(".field-field-com-processo")[0].text_content())) if root3.cssselect(".field-field-com-processo") else '',
        'comp_sistema' : (text(root3.cssselect(".field-field-com-sistema")[0].text_content())) if root3.cssselect(".field-field-com-sistema") else '',
        'professioni' : (implode(root3.cssselect(".field-field-professione"), 'Attività formativa per :'.decode('utf8'))) if root3.cssselect(".field-field-professione") else '',
        'discipline' : (implode(root3.cssselect(".field-field-discipline"), 'Discipline di riferimento:')) if root3.cssselect(".field-field-discipline") else '',
        'localita' : '',
        'last_data' : dateiso(root3.cssselect('.submitted')[0].text_content().split(' il ')[1]),
        'titolo' : root3.cssselect("h1.title")[0].text_content() if root3.cssselect("h1.title") else ''

          
    }

    
    scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name='mydata')

    



    