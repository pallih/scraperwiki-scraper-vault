#Scraper for Thailand's Member of House of Representative.

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://mp.parliament.go.th/Biographical/FrontWeb/Human_Resource/PersonList.aspx')
soup = BeautifulSoup(html)
table = soup.find(id='gvHumanList')
for tr in table.findAll('tr')[1:]:
    td = tr.findAll('td')
    link = td[4].find('a')
    #print td[1].text, td[2].contents[0].text, td[3].text, link['href']
    print td[1].string.strip(), td[2].contents[0].string.strip(), td[3].string.strip(), link['href']

    try:
        bio_html = scraperwiki.scrape(link['href'])
    except:
        print "ERROR: cannot fetch ", link['href']
        continue

    bio_soup = BeautifulSoup(bio_html)
    img = bio_soup.find(id='DataList5_ctl00_Image1')
    addr = {}
    addr['address'] = bio_soup.find(id='DataList3_ctl00_P_ADDRESSLabel').string
    addr['moo'] = bio_soup.find(id='DataList3_ctl00_P_MOOLabel').string
    addr['mooban'] = bio_soup.find(id='DataList3_ctl00_P_MOO_BANLabel').string
    addr['soi'] = bio_soup.find(id='DataList3_ctl00_P_SOILabel').string
    addr['road'] = bio_soup.find(id='DataList3_ctl00_P_ROADLabel').string
    addr['tambol'] = bio_soup.find(id='DataList3_ctl00_P_TAMBOLLabel').string
    addr['amphur'] = bio_soup.find(id='DataList3_ctl00_P_AMPHURLabel').string
    addr['province'] = bio_soup.find(id='DataList3_ctl00_Label2').string
    addr['zipcode'] = bio_soup.find(id='DataList3_ctl00_P_ZIPCODELabel').string
    addr['telno'] = bio_soup.find(id='DataList3_ctl00_P_TELEPHONELabel').string
    addr['faxno'] = bio_soup.find(id='DataList3_ctl00_P_FAXLabel').string
    addr['email'] = bio_soup.find(id='DataList3_ctl00_P_E_MAILLabel').string
    
    record = { 'name': td[1].string, 'party': td[2].contents[0].string, 'area': td[3].string, 'addr': addr }
    scraperwiki.datastore.save(['name'], record)