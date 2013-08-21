# http://webapp.etsi.org/WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE&qSORT=HIGHVERSION&qINCLUDE_SUB_TB=True&qREPORT_TYPE=SUMMARY&optDisplay=1000&includeNonActiveTB=FALSE&qOFFSET=100

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

limit = 100
searchURL = 'http://webapp.etsi.org/WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE&qSORT=HIGHVERSION&qINCLUDE_SUB_TB=True&qREPORT_TYPE=SUMMARY&optDisplay='+str(limit)
wkiURL = 'http://webapp.etsi.org/WorkProgram/Report_WorkItem.asp?'
scheduleURL = 'http://webapp.etsi.org/workProgram/Report_Schedule.asp?'
translationURL = 'http://webapp.etsi.org/net/transposition/TranslationListView.aspx?'

def scrape_search_page(offset):
    html = scraperwiki.scrape(searchURL +'&qOFFSET='+str(offset))
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    tables = html.findAll('table')
    rows = tables[3].findAll('tr')
    for i in range(1,len(rows)):
        cols = rows[i].findAll('td')
        a = cols[1].find('a', href=re.compile("Report_WorkItem\\.asp\\?WKI_ID=.*"))
        match = re.search( r'Report_WorkItem\.asp\?WKI_ID=(\d+).*', a['href'], re.M|re.I)
        if match:
            id = int(match.group(1))
            try:
                wki = scrape_work_item(id)
                scrape_schedule(id)
                if wki['harmonized_standard']:
                    scrape_title_translation(id)
            except:
                print "error for WKI_ID:"+ str(id)
                
def scrape_work_item(id):
    wki = {'id': id}
    html = scraperwiki.scrape(wkiURL+'WKI_ID='+str(id))
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    divs = html.findAll('div')
    rows = divs[1].find('table').findAll('tr')
    cols = rows[1].findAll('td')
    wki['reference'] = cols[1].text
    wki['etsi_doc_nb'] = cols[2].text
    wki['stf'] = cols[3].text
    wki['technical_body'] = cols[4].text
    cols = rows[3].findAll('td')
    wki['cover_date'] = cols[3].text
    wki['creation_date'] = cols[5].text
    cols = rows[5].findAll('td')
    wki['rapporteur'] = cols[1].text
    wki['technical_officer'] = cols[2].text
    wki['harmonized_standard'] = cols[3].text.find('Yes')!=-1
    cols = rows[7].findAll('td')
    wki['title'] = cols[1].text
    cols = rows[8].findAll('td')
    wki['scope'] = cols[1].text
    cols = rows[9].findAll('td')
    supporting_organizations = cols[1].text.replace(',',';')
    wki['supporting_organizations'] = supporting_organizations.split('; ')
    rows = divs[3].find('table').findAll('tr')
    cols = rows[1].findAll('td')
    wki['keywords'] = []
    for item in cols[1].findAll('br'):
        wki['keywords'].append(item.previousSibling)
    wki['projects'] = []
    for item in cols[2].findAll('br'):
        wki['projects'].append(item.previousSibling)
    wki['mandates'] = []
    for item in cols[3].findAll('br'):
        wki['mandates'].append(item.previousSibling)
    wki['directives'] = []
    for item in cols[4].findAll('br'):
        wki['directives'].append(item.previousSibling)
    scraperwiki.sqlite.save(unique_keys=['id'], data = wki,table_name="work_items")
    return wki

def scrape_schedule(id):
    html = scraperwiki.scrape(scheduleURL +'WKI_ID='+str(id))
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    divs = html.findAll('div')
    rows = divs[1].find('table').findAll('tr')
    for i in range(1,len(rows)):
        status = {'wki_id':id}
        cols = rows[i].findAll('td')
        status['status'] = cols[0].text
        status['milestone'] = cols[1].text
        status['action'] = cols[2].text
        status['action_nb'] = cols[3].text
        status['target'] = cols[4].text
        status['achieved'] = cols[5].text
        status['version'] = cols[6].text
        scraperwiki.sqlite.save(unique_keys=['wki_id','status'], data = status,table_name="schedule")
def scrape_title_translation(id):
    html = scraperwiki.scrape(translationURL +'WKI_ID='+str(id))
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[0]
    rows = table.findAll('tr')
    for i in range(1,len(rows)):
        entry = {'wki_id':id}
        cols = rows[i].findAll('td')
        entry['country'] = cols[0].text
        entry['title'] = cols[1].text
        scraperwiki.sqlite.save(unique_keys=['wki_id','country'], data = entry,table_name="translations")

if scraperwiki.sqlite.get_var('offset') == None:
    scraperwiki.sqlite.save_var('offset',0)
offset = scraperwiki.sqlite.get_var('offset')
while offset < 36000:
    scrape_search_page(offset)
    scraperwiki.sqlite.save_var('offset',offset)
    offset = offset+limit

#scrape_work_item(13878);
#scrape_schedule(13878);
#scrape_title_translation(13878);