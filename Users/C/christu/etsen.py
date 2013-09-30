import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

baseURL = 'http://webapp.etsi.org/'
name = "Identification"
indicator = "Title"
unit = "Status"

def run():
    html = scraperwiki.scrape(baseURL+ 'WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE&butExpertSearch=++Search++&qETSI_STANDARD_TYPE=&qETSI_NUMBER=&qTB_ID=&qINCLUDE_SUB_TB=True&includeNonActiveTB=FALSE&qWKI_REFERENCE=&qTITLE=&qSCOPE=&qCURRENT_STATE_CODE=&qSTOP_FLG=N&qSTART_CURRENT_STATUS_CODE=&qEND_CURRENT_STATUS_CODE=&qFROM_MIL_DAY=&qFROM_MIL_MONTH=&qFROM_MIL_YEAR=&qTO_MIL_DAY=&qTO_MIL_MONTH=&qTO_MIL_YEAR=&qOPERATOR_TS=&qRAPTR_NAME=&qRAPTR_ORGANISATION=&qKEYWORD_BOOLEAN=OR&qKEYWORD=&qPROJECT_BOOLEAN=OR&qPROJECT_CODE=&includeSubProjectCode=FALSE&qSTF_List=&qDIRECTIVE=&qMandate_List=&qSORT=HIGHVERSION&qREPORT_TYPE=SUMMARY&optDisplay=10&titleType=all')
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        href = cols[0].find('a')['href']
        state = cols[1].text
        try:
            scrape_site(baseURL+href,state)
        except:
            print "error "+ baseURL+href
            pass

def scrape_site(url,state):
    d = date.today()-timedelta(days=1)
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        observation = {}
        observation['Identification'] = cols[1].text
        observation['Title'] = Indicator
        observation['Status'] = unit
        # observation['unit'] = unit
        observation['date'] = d
        # observation['state'] = state
        try:
            observation['Identification'] = float(cols[2].text)
        except ValueError:
            observation['Identification'] = None
        try:
            observation['value'] = float(cols[3].text)
        except ValueError:
            observation['value'] = None
        scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
        print observation
import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

baseURL = 'http://webapp.etsi.org/'
name = "Identification"
indicator = "Title"
unit = "Status"

def run():
    html = scraperwiki.scrape(baseURL+ 'WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE&butExpertSearch=++Search++&qETSI_STANDARD_TYPE=&qETSI_NUMBER=&qTB_ID=&qINCLUDE_SUB_TB=True&includeNonActiveTB=FALSE&qWKI_REFERENCE=&qTITLE=&qSCOPE=&qCURRENT_STATE_CODE=&qSTOP_FLG=N&qSTART_CURRENT_STATUS_CODE=&qEND_CURRENT_STATUS_CODE=&qFROM_MIL_DAY=&qFROM_MIL_MONTH=&qFROM_MIL_YEAR=&qTO_MIL_DAY=&qTO_MIL_MONTH=&qTO_MIL_YEAR=&qOPERATOR_TS=&qRAPTR_NAME=&qRAPTR_ORGANISATION=&qKEYWORD_BOOLEAN=OR&qKEYWORD=&qPROJECT_BOOLEAN=OR&qPROJECT_CODE=&includeSubProjectCode=FALSE&qSTF_List=&qDIRECTIVE=&qMandate_List=&qSORT=HIGHVERSION&qREPORT_TYPE=SUMMARY&optDisplay=10&titleType=all')
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        href = cols[0].find('a')['href']
        state = cols[1].text
        try:
            scrape_site(baseURL+href,state)
        except:
            print "error "+ baseURL+href
            pass

def scrape_site(url,state):
    d = date.today()-timedelta(days=1)
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        observation = {}
        observation['Identification'] = cols[1].text
        observation['Title'] = Indicator
        observation['Status'] = unit
        # observation['unit'] = unit
        observation['date'] = d
        # observation['state'] = state
        try:
            observation['Identification'] = float(cols[2].text)
        except ValueError:
            observation['Identification'] = None
        try:
            observation['value'] = float(cols[3].text)
        except ValueError:
            observation['value'] = None
        scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
        print observation
