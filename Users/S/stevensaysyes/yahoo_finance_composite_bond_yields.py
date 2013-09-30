import scraperwiki
import lxml.html
from datetime import date

bond_types = ['US Treasury', 'Municipal', 'Corporates']
data = {}
data['Date'] = date.today()

html = scraperwiki.scrape('http://finance.yahoo.com/bonds/composite_bond_rates')
root = lxml.html.fromstring(html)

i = -1
for tr in root.cssselect('div[class="yfirateswrp yfimhdg"] tr'):
    tds = tr.cssselect('td')
    row = [td.text_content() for td in tds]
    if row == []:
        i += 1
        continue
    
    data['Type'] = bond_types[i]
    if data['Type'] == 'US Treasury':
        data['Maturity'] = row[0]
        data['Rating'] = 'Treasury'
    else:
        data['Maturity'], data['Rating'] = row[0].split(' ')
    data['Yield Today'], data['Yield Yesterday'], data['Yield Last Week'], data['Yield Last Month'] = row[1:5]
    scraperwiki.sqlite.save(unique_keys=['Type','Date', 'Maturity', 'Rating'], data=data)import scraperwiki
import lxml.html
from datetime import date

bond_types = ['US Treasury', 'Municipal', 'Corporates']
data = {}
data['Date'] = date.today()

html = scraperwiki.scrape('http://finance.yahoo.com/bonds/composite_bond_rates')
root = lxml.html.fromstring(html)

i = -1
for tr in root.cssselect('div[class="yfirateswrp yfimhdg"] tr'):
    tds = tr.cssselect('td')
    row = [td.text_content() for td in tds]
    if row == []:
        i += 1
        continue
    
    data['Type'] = bond_types[i]
    if data['Type'] == 'US Treasury':
        data['Maturity'] = row[0]
        data['Rating'] = 'Treasury'
    else:
        data['Maturity'], data['Rating'] = row[0].split(' ')
    data['Yield Today'], data['Yield Yesterday'], data['Yield Last Week'], data['Yield Last Month'] = row[1:5]
    scraperwiki.sqlite.save(unique_keys=['Type','Date', 'Maturity', 'Rating'], data=data)