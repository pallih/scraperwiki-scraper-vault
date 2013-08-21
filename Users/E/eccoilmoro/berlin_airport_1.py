from urllib2 import urlparse


import scraperwiki
import lxml.html
import datetime


SITEPAGE =   'http://albopretorio.comune.lugo.ra.it/?ente=unione'
URL_ALLEGATI = 'http://albopretorio.comune.lugo.ra.it/'
ENTE_ALLEGATI = '1' #1 Unione 0 Comune di Lugo

def get_details_from_url(url_portion):
    res = urlparse.parse_qs(url_portion.partition('?')[2])
    if not res: # might happen in the case of someone not submitting a URL with "details.php?" at the start
        res = url_portion 
    for key in res.keys():
        res[key] = res[key][0]
    return res

def get_alternate_flights(row):
    print row[-1].text, row[-1].text_content()
    return row[-1].text.partition(': ')[2] or ''

def get_carrier(row):
    td = row.cssselect('a.linkbold')[0]
    carrier = td.attrib['title'].rsplit('(')[-1][:-1]
    return carrier or '' 

def get_date(row):
    return row.text_content().replace(u'\xa0', ' ').strip() or ''

def is_codeshare(row):
    return any('codeshare' in img.attrib['alt'] for img in row.iterdescendants('img'))

def is_date(row):
    return len(row.cssselect('th')) == 2

def is_column_heading(row):
    return 'Flug' in row.text_content()

def parse_page(url):
    root = lxml.html.parse(url).getroot()
    if root is not None:
        print("nell albero")
        for table in root.cssselect('table'):
             print(table.attrib['summary']+'weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
             count = 0 
             for row in table.cssselect('tbody tr'):
                #print(row)
                try:
                    if len(row)>1:
                        #print(row[4].text)
                        riga = {}
                        if table.attrib['summary'] == 'Altri Atti' :
                            riga["tipodoc"]  = row[1].text.replace(u'\xa0', ' ').strip()
                            if 'non' in row[0].text:
                                riga["key"] = 'n'+count
                                print riga["key"].text
                                count = count + 1
                            else:
                                riga["key"] = row[0].text
                            riga["oggetto"] = row[2].text.encode('utf-8').replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            riga["datapubbfrom"] = row[3].text_content().replace(u'\xa0', ' ').strip() or ''
                            
                        else :
                            riga["tipodoc"]  = table.attrib['summary'] 
                            riga["key"] = row[3].text.replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            riga["oggetto"] = row[4].text.decode('utf-8').replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            riga["datapubbfrom"] = row[5].text_content().replace(u'\xa0', ' ').strip() or ''
                        allegato = ''
                        if row.cssselect('img') :
                               img=row.cssselect('img')
                               if len(img[0].attrib['onclick'])>1:
                                   index= img[0].attrib['onclick'].find(',')
                                   allegato = img[0].attrib['onclick'][24:index-1]
                               else:
                                   print('purachio')
                               riga["URL_allegato"] = URL_ALLEGATI + allegato
                        print(riga)
                        scraperwiki.sqlite.save(unique_keys=["key"], data=riga)
                except:
                #   print('errore') 
                   continue
                   # riga["id"]    = row[2].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                   # riga["oggetto"]      = row[3].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                   # riga["datapubbfrom"]      = row[4].text or ''
                   # riga["datapubbto"] = row[5].text or ''
                   # riga["allegati"]  = row[6].text or ''

#            if is_date(row):
#                date = get_date(row)
#                continue
#            elif is_codeshare(row):
#                flight = previous_flight
#                flight['alt_flights'] = get_alternate_flights(row)
#            elif len(row) < 8 or is_column_heading(row):
#               continue
#            else:
#                flight = {}
#                flight["no"]        = row[1].text_content().replace(u'\xa0', ' ')
#                flight["c_from"]    = row[2].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
#                flight["c_to"]      = row[3].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
#                flight["gate"]      = row[4].text or ''
#                flight["scheduled"] = row[5].text or ''
#                flight["expected"]  = row[6].text or ''
#                flight["state"]     = row[7].text or ''
#                flight["carrier"]   = get_carrier(row)
#                flight["date"]      = date or ''
#                flight['alt_flights'] = ''
#                flight['date_scraped'] = datetime.datetime.today()
#                for key, val in get_details_from_url(row[1].cssselect('a.linkbold')[0].attrib['href']).iteritems():
#                    flight[key] = val
            #scraperwiki.sqlite.save(unique_keys=["no"], data=flight)
                   
#            previous_flight = flight
#        if len(root.cssselect('.content_barrightbottom a')) > 0:
#            return root.cssselect('.content_barrightbottom a')[0].attrib['href']
#        else:
#            return None
#    else:
#       return None

def main():
    scraperwiki.sqlite.execute("drop table if exists swdata")
    scraperwiki.sqlite.commit()
    parse_page(SITEPAGE)
main()
