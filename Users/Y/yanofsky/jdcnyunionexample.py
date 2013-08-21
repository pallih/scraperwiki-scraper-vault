from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring
import datetime


#List of Column Names We Will Use
COLNAMES=[
        'employer',
        'download',
        'location',
        'union',
        'local',
        'naics',
        'num_workers',
        'expiration_date'
  ]

#List of State codes for error checking
STATES =[ 'Na',
      'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
      'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
      'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
      'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
      'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

BASEURL = "http://www.dol.gov/olms/regs/compliance/cba/"

#url list
URLS = [
 "Cba_AaAg.htm" ,
 "Cba_AiAz.htm" ,
 "Cba_BaBo.htm" ,
 "Cba_BpBz.htm" ,
 "Cba_CaCn.htm" ,
 "Cba_CoCz.htm" ,
 "Cba_DaEz.htm" ,
 "Cba_FaGo.htm" ,
 "Cba_GpHz.htm" ,
 "Cba_IaJz.htm" ,
 "Cba_KaKz.htm" ,
 "Cba_LaMa.htm" ,
 "Cba_MbMz.htm" ,
 "Cba_NaNe.htm" ,
 "Cba_NfOz.htm" ,
 "Cba_PaPz.htm" ,
 "Cba_QaRz.htm" ,
 "Cba_SaSm.htm" ,
 "Cba_SnSz.htm" ,
 "Cba_TaUz.htm" ,
 "Cba_VaZz.htm" ,
 "Cbau_aabz.htm",
 "Cbau_cach.htm",
 "Cbau_cicz.htm",
 "Cbau_dadz.htm",
 "Cbau_eagz.htm",
 "Cbau_haiz.htm",
 "Cbau_jakz.htm",
 "Cbau_lalz.htm",
 "Cbau_mamh.htm",
 "Cbau_mimz.htm",
 "Cbau_nane.htm",
 "Cbau_nene.htm",
 "Cbau_nenz.htm",
 "Cbau_oaoz.htm",
 "Cbau_papz.htm",
 "Cbau_qarz.htm",
 "Cbau_sasa.htm",
 "Cbau_sasz.htm",
 "Cbau_tavz.htm",
 "Cbau_wazz.htm"
]

#Targeted URL
URL="http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm"

def saveFilingTable(url):
    #scrape the url
    raw=scrape(url)
    
    #parse the scrape
    parsed = fromstring(raw)
    
    #find the target table
    trgTable = parsed.cssselect("table")[2]
    
    #extract all the rows
    rows = trgTable.cssselect("tr")
    
    #loop through each row
    for row in rows[1:]:
        cells = row.cssselect("td,th")
        cellcontents = [cell.text_content() for cell in cells]
        data = dict(zip(COLNAMES,cellcontents))
        data['num_workers'] = int(data['num_workers'])
        data['state'] = data['location'].strip()[0:2]
        if data['state'] not in STATES:
            data['state'] = 'unknown'
        
        v = map(int,data['expiration_date'].split('-'))
        data['expiration_date'] = datetime.date(v[2]+2000,v[0],v[1])

        save([],data)

for url in URLS:
    saveFilingTable(BASEURL+url)

