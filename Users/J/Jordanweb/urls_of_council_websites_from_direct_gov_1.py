import scraperwiki
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse,parse_qs


start_page = "http://www.direct.gov.uk/en/Dl1/Directories/Localcouncils/AToZOfLocalCouncils/index.htm"

council_list = BeautifulSoup(scraperwiki.scrape(start_page))
a_to_z_list = council_list.find('ul', {'class': 'atoz'}).findAll('a')

council_list_page_urls = [(start_page + x['href']) for x in a_to_z_list]

existing_council_urls = set()
if 'swdata' in scraperwiki.sqlite.show_tables():
    existing_council_urls = set([x['url'] for x in scraperwiki.sqlite.select("* from swdata")])

council_page_urls = []
new_council_urls = set()

for council_list_page_url in council_list_page_urls:
    list_page_html = BeautifulSoup(scraperwiki.scrape(council_list_page_url))
    main_list = list_page_html.find('div', {'id': 'dgr11'}).findAll('div', {'class': 'subContent'})
    council_page_urls = council_page_urls + [('http://www.direct.gov.uk/%s' % x) for x in [y.find('a')['href'] for y in main_list] if x[0] == u'/'] 

for council_page_url in council_page_urls:
    soup = BeautifulSoup(scraperwiki.scrape(council_page_url))
    url = soup.find('a', {'class':'externalLink'})['href']
    name = soup.find('div', {'class': 'introContent'}).find('h2').string
    new_council_urls.add(url)
    scraperwiki.sqlite.save(unique_keys=['url'], data={'council_name': name, 'url': url})

councils_to_remove = existing_council_urls - new_council_urls

for url in councils_to_remove:
    scraperwiki.sqlite.execute('DELETE FROM swdata WHERE url = ?', [url])

scraperwiki.sqlite.commit()