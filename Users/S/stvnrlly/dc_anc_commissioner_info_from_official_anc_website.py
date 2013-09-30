import scraperwiki
import lxml.html           
import re

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`smd` text, `last_name` text, `first_name` text, `suffix` text, `address` text, `zip` text, `phone` text, `email` text, `ward` text, `anc` text)')
html = scraperwiki.scrape('http://anc.dc.gov')
root = lxml.html.fromstring(html)
for a in root.cssselect('li.leaf > a'):
    text = a.text_content()
    if not re.search('^ANC \d[A-Z]$', text):
        continue
    url = 'http://anc.dc.gov' + a.attrib['href']
    html = scraperwiki.scrape(url)
    table = lxml.html.fromstring(html).cssselect('table').pop()
    for row in table.cssselect("tbody tr"):
        cells = row.cssselect('td')
        rec = {}
        rec['smd'] = cells[0].text_content()
        name = cells[1].text_content().strip()
        name = re.sub(u'\xa0', ' ', name)
        m = re.search('^\s*(\S.*?) (\S+?)(?:,? (Jr|Sr|I+)\.?)?\s*$', name)
        if not m:
            rec['first_name'] = ''
            rec['last_name'] = name
            rec['suffix'] = ''
        else:
            rec['first_name'] = (m.group(1) or '')
            rec['last_name'] = (m.group(2) or '')
            rec['suffix'] = (m.group(3) or '')
        rec['address'] = cells[2].text_content()
        m = re.search('DC\s+([\d-]+)', rec['address'])
        if m:
            rec['zip'] = m.group(1)
        else:
            rec['zip'] = ''
        rec['address'] = re.sub('\s*Washington[,\s\xa0]*DC(?:\s+([\d-]+))?', '', rec['address'])
        rec['address'] = re.sub(', (?=[NS][EW])', ' ', rec['address'])
        print len(cells[3].text_content())
        if len(cells[3].text_content()) <= 7:
            rec['phone'] = ''
        elif len(cells[3].text_content()) <= 14:
            rec['phone'] = '202-' + cells[3].text_content()
        else:
            rec['phone'] = cells[3].text_content()
        rec['email'] = cells[4].text_content()
        for k in rec.keys():
            rec[k] = re.sub('^ | $', '', re.sub('\s+', ' ', re.sub(u'\xa0', ' ', rec[k])))
        rec['ward'] = rec['smd'][:1]
        rec['anc'] = rec['smd'][:2]
        scraperwiki.sqlite.save(['smd'], rec)import scraperwiki
import lxml.html           
import re

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`smd` text, `last_name` text, `first_name` text, `suffix` text, `address` text, `zip` text, `phone` text, `email` text, `ward` text, `anc` text)')
html = scraperwiki.scrape('http://anc.dc.gov')
root = lxml.html.fromstring(html)
for a in root.cssselect('li.leaf > a'):
    text = a.text_content()
    if not re.search('^ANC \d[A-Z]$', text):
        continue
    url = 'http://anc.dc.gov' + a.attrib['href']
    html = scraperwiki.scrape(url)
    table = lxml.html.fromstring(html).cssselect('table').pop()
    for row in table.cssselect("tbody tr"):
        cells = row.cssselect('td')
        rec = {}
        rec['smd'] = cells[0].text_content()
        name = cells[1].text_content().strip()
        name = re.sub(u'\xa0', ' ', name)
        m = re.search('^\s*(\S.*?) (\S+?)(?:,? (Jr|Sr|I+)\.?)?\s*$', name)
        if not m:
            rec['first_name'] = ''
            rec['last_name'] = name
            rec['suffix'] = ''
        else:
            rec['first_name'] = (m.group(1) or '')
            rec['last_name'] = (m.group(2) or '')
            rec['suffix'] = (m.group(3) or '')
        rec['address'] = cells[2].text_content()
        m = re.search('DC\s+([\d-]+)', rec['address'])
        if m:
            rec['zip'] = m.group(1)
        else:
            rec['zip'] = ''
        rec['address'] = re.sub('\s*Washington[,\s\xa0]*DC(?:\s+([\d-]+))?', '', rec['address'])
        rec['address'] = re.sub(', (?=[NS][EW])', ' ', rec['address'])
        print len(cells[3].text_content())
        if len(cells[3].text_content()) <= 7:
            rec['phone'] = ''
        elif len(cells[3].text_content()) <= 14:
            rec['phone'] = '202-' + cells[3].text_content()
        else:
            rec['phone'] = cells[3].text_content()
        rec['email'] = cells[4].text_content()
        for k in rec.keys():
            rec[k] = re.sub('^ | $', '', re.sub('\s+', ' ', re.sub(u'\xa0', ' ', rec[k])))
        rec['ward'] = rec['smd'][:1]
        rec['anc'] = rec['smd'][:2]
        scraperwiki.sqlite.save(['smd'], rec)