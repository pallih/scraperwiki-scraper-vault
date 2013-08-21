import scraperwiki

from urllib2 import urlparse


import scraperwiki
import lxml.html
import datetime


SITEPAGE =   'http://albopretorio.comune.lugo.ra.it/?ente=fusignano'
URL_ALLEGATI = 'http://albopretorio.comune.lugo.ra.it/'
#ENTE_ALLEGATI = '1' #1 Unione 0 Comune di Lugo



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
                print("Riga" + row[0].text)
                try:
                    if len(row)>1:
                        #print(row[4].text)
                        riga = {}
                        if table.attrib['summary'] == 'Altri Atti' :
                            riga["tipodoc"]  = row[2].text.replace(u'\xa0', ' ').strip()
                            if 'non' in row[0].text:
                                riga["key"] = 'n' + str(count)
                                print riga["key"]
                                count = count + 1
                            else:
                                riga["key"] = row[0].text
                            try:
                                riga["oggetto"] = row[3].text.encode('utf-8',errors='ignore').replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            except:
                                print("Errore encode")
                                continue
                            riga["datapubbfrom"] = row[4].text_content().replace(u'\xa0', ' ').strip() or ''
                            riga["datapubbto"] = row[5].text_content().replace(u'\xa0', ' ').strip() or ''
                        else :
                            riga["tipodoc"]  = table.attrib['summary']
                            riga["key"] = row[0].text.replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            #riga["oggetto"] = row[4].text.decode('utf-8',errors='ignore')
                            try:
                                riga["oggetto"] = row[5].text.encode('utf-8',errors='ignore').replace('\r\n', ' ').replace('\t\t\t',' ').strip()
                            except:
                                print("Errore encode")
                                continue
                            riga["datapubbfrom"] = row[6].text_content().replace(u'\xa0', ' ').strip() or ''
                            riga["datapubbto"] = row[7].text_content().replace(u'\xa0', ' ').strip() or ''
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
                   print('errore')
                   #continue
                   # riga["id"]    = row[2].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                   # riga["oggetto"]      = row[3].text.encode('utf-8').replace("\xc2\xa0", " ") or ''
                   # riga["datapubbfrom"]      = row[4].text or ''
                   # riga["datapubbto"] = row[5].text or ''
                   # riga["allegati"]  = row[6].text or ''


def main():
    scraperwiki.sqlite.execute("drop table if exists swdata")
    scraperwiki.sqlite.commit()
    parse_page(SITEPAGE)
main()


