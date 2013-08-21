# Load Union Square Ventures investments into Fluidinfo

# (WORK IN PROGRESS)

import scraperwiki
import lxml.etree
import lxml.html
import fom.session

fdb = fom.session.Fluid()
fdb.login('scraperwiki', 'Aev0eari')

# load one set of investments (current or past) in
def load_investments(investments, is_current):
    for i in investments.cssselect('li'):
        data = {}
        data['name'] = i.cssselect('.holder-heading strong')[0].text
        data['details'] = i.cssselect('.frame a')[0].get('href')
        data['logo'] = i.cssselect('.frame img')[0].get('src')
        data['current'] = is_current

        fdb.about[data['details']]['scraperwiki/unionsquareventures.com/investments'].put(True)

# extract portfolio / past investment blocks
html = scraperwiki.scrape("http://www.usv.com/investments/")
root = lxml.html.fromstring(html) # an lxml.etree.Element object

investments = root.cssselect("ul.investments")
current = investments[0]
past = investments[1]

load_investments(current, True)
#load_investments(past, False, )


