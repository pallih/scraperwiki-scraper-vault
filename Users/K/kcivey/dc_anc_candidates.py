import scraperwiki
import lxml.html
import dateutil.parser           
import re

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`id` integer, `smd` text, `last_name` text, `first_name` text, `suffix` text, `pickup_date` text, `filing_date` text, `address` text, `zip` text, `phone` text, `email` text, `ward` text, `anc` text)')
html = scraperwiki.scrape('http://www.dcboee.org/newsroom/showASPfile.asp?cat=News%20Releases&id=1013&mid=7&yid=2012')
root = lxml.html.fromstring(html)
id = 0;
for row in root.cssselect('table[width=1309] tr'):
    rec = {}
    cells = row.cssselect('td')
    first_cell = cells[0].text_content().strip();
    m = re.search('^((([1-8])[A-M])[01]\d)$', first_cell)
    if not m:
        if not re.search('^[1-8][A-M]$', first_cell) and not first_cell == 'ANC/SMD':
            print 'Unexpected format :"' + first_cell + '"'
        continue
    id += 1
    rec['id'] = id
    rec['smd'] = m.group(0)
    rec['anc'] = m.group(1)
    rec['ward'] = m.group(2)
    name = cells[1].text_content()
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
    rec['address'] = re.sub(', (?=[NS][EW])', ' ', rec['address'])
    rec['zip'] = cells[3].text_content()
    rec['phone'] = re.sub('\s+', '', cells[4].text_content())
    if re.search('^\d{3}-\d{4}$', rec['phone']):
        rec['phone'] = '202-' + rec['phone']
    rec['pickup_date'] = cells[5].text_content()
    rec['filing_date'] = cells[6].text_content()
    rec['email'] = cells[7].text_content()
    for k in rec.keys():
        if k != 'id':
            rec[k] = re.sub('^ | $', '', re.sub('\s+', ' ', re.sub(u'\xa0', ' ', rec[k])))
    for k in ['pickup_date', 'filing_date']:
        if rec[k] != '':
            rec[k] = dateutil.parser.parse(rec[k]).date()
    scraperwiki.sqlite.save(['id'], rec)