import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach('defence-contracts-all')

scraperwiki.sqlite.select ("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping('url')
    print url

    soup = BeautifulSoup(scraping['html'])

    title = soup.find('div', 'fieldset-title corners-top').get_text().replace('English','').strip
    print title

ps = soup.find_all ('p', 'clearfix')

for p in ps:
    span_text = ""
    span = p.find


<p class="clearfix">


