import scraperwiki
import lxml.html
import re
html = scraperwiki.scrape("http://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;db=HANDBOOK;id=handbook%2Fnewhandbook%2F2008-12-19%2F0074;query=Id%3A%22handbook%2Fnewhandbook%2F2008-12-19%2F0071%22")         
root = lxml.html.fromstring(html)
for table in root.xpath("//div[@class='docDiv']/table")[0]:
    header = table.cssselect('tr')[0]
    parties = [re.match(r'[a-zA-Z\-]+', party.text_content()).group(0) for party in header.cssselect('td p')[2:-1]]
    for row in table.cssselect('tr')[1:]:
        day, month, year = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', row.cssselect('td p')[0].text_content()).group(0).split('.')
        date = '%s/%s/%s' % (month.zfill(2), day.zfill(2), year)
        data = {}
        cell_num = 0
        data['date'] = date
        for cell in row.cssselect('td p')[2:-1]:
            content = cell.text_content()
            if content != '-':
                content = re.search(r'\d+', cell.text_content()).group(0)
                data[str(parties[cell_num])] = int(content)
            else:
                data[str(parties[cell_num])] = 0
            cell_num += 1
        print data
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)

import scraperwiki
import lxml.html
import re
html = scraperwiki.scrape("http://parlinfo.aph.gov.au/parlInfo/search/display/display.w3p;db=HANDBOOK;id=handbook%2Fnewhandbook%2F2008-12-19%2F0074;query=Id%3A%22handbook%2Fnewhandbook%2F2008-12-19%2F0071%22")         
root = lxml.html.fromstring(html)
for table in root.xpath("//div[@class='docDiv']/table")[0]:
    header = table.cssselect('tr')[0]
    parties = [re.match(r'[a-zA-Z\-]+', party.text_content()).group(0) for party in header.cssselect('td p')[2:-1]]
    for row in table.cssselect('tr')[1:]:
        day, month, year = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', row.cssselect('td p')[0].text_content()).group(0).split('.')
        date = '%s/%s/%s' % (month.zfill(2), day.zfill(2), year)
        data = {}
        cell_num = 0
        data['date'] = date
        for cell in row.cssselect('td p')[2:-1]:
            content = cell.text_content()
            if content != '-':
                content = re.search(r'\d+', cell.text_content()).group(0)
                data[str(parties[cell_num])] = int(content)
            else:
                data[str(parties[cell_num])] = 0
            cell_num += 1
        print data
        scraperwiki.sqlite.save(unique_keys=['date'], data=data)

