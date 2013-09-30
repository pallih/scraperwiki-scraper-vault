import scraperwiki
from BeautifulSoup import BeautifulSoup
print 'The colleges in hyderabad'
base_url='http://www.jntuhaac.com'
page_url='/allcolleges.php?district=HYDERABAD'
while True:
    html=scraperwiki.scrape(base_url+page_url)
    soup=BeautifulSoup(html)
    tables = soup.findAll('table')
    rows = tables[5].findAll('tr')
    for row in rows:
        record = {}
        table_cells = row.findAll('td')
        if table_cells:
            record['S.no'] = table_cells[0].text
            record['Code'] = table_cells[1].text
            record['CollegeName'] = table_cells[2].text
            record['URL'] = table_cells[3].text
            record['District'] = table_cells[4].text
            print record, '------------'
            scraperwiki.sqlite.save(['CollegeName'], record)
    last_link=soup.findAll('a', 'small_link')[-1]
    if not last_link.text.find('Next')<0:
        page_url = last_link['href']
        print last_link['href']
    else:
        break


import scraperwiki
from BeautifulSoup import BeautifulSoup
print 'The colleges in hyderabad'
base_url='http://www.jntuhaac.com'
page_url='/allcolleges.php?district=HYDERABAD'
while True:
    html=scraperwiki.scrape(base_url+page_url)
    soup=BeautifulSoup(html)
    tables = soup.findAll('table')
    rows = tables[5].findAll('tr')
    for row in rows:
        record = {}
        table_cells = row.findAll('td')
        if table_cells:
            record['S.no'] = table_cells[0].text
            record['Code'] = table_cells[1].text
            record['CollegeName'] = table_cells[2].text
            record['URL'] = table_cells[3].text
            record['District'] = table_cells[4].text
            print record, '------------'
            scraperwiki.sqlite.save(['CollegeName'], record)
    last_link=soup.findAll('a', 'small_link')[-1]
    if not last_link.text.find('Next')<0:
        page_url = last_link['href']
        print last_link['href']
    else:
        break


