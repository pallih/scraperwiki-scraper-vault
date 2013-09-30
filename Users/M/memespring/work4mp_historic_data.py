import time
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

page = 4300
while page <= 9500:

    url = 'http://www.w4mp.org/html/personnel/jobs/disp_job_text.asp?ref=%s' % page
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    table = soup.find('table').find('table')

    def soup_strip_html(st):
        return ''.join([e.strip() for e in st.recursiveChildGenerator() if isinstance(e,unicode)])

    def strip_html(st):
        tags = re.compile(r'<.*?>')
        return tags.sub('',st)
    
    if table:
        data = {}
        data['url'] = url
        row_count = 0
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if row_count == 1:
                key = 'title'
                data[key] = soup_strip_html(cells[0])
            else:
                if cells[0].string != '&nbsp;' and cells[1].string != '&nbsp;':
                    key = soup_strip_html(cells[0])
                    value = None
                    if key == 'Website':
                        value = cells[1].a['href']
                    else:
                        value = soup_strip_html(cells[1])
        
                    data[key] = value
                
            row_count = row_count + 1
        
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    #sleep for a couple of secs to we don't break anything
    time.sleep(2)
    page = page + 1import time
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

page = 4300
while page <= 9500:

    url = 'http://www.w4mp.org/html/personnel/jobs/disp_job_text.asp?ref=%s' % page
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    table = soup.find('table').find('table')

    def soup_strip_html(st):
        return ''.join([e.strip() for e in st.recursiveChildGenerator() if isinstance(e,unicode)])

    def strip_html(st):
        tags = re.compile(r'<.*?>')
        return tags.sub('',st)
    
    if table:
        data = {}
        data['url'] = url
        row_count = 0
        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if row_count == 1:
                key = 'title'
                data[key] = soup_strip_html(cells[0])
            else:
                if cells[0].string != '&nbsp;' and cells[1].string != '&nbsp;':
                    key = soup_strip_html(cells[0])
                    value = None
                    if key == 'Website':
                        value = cells[1].a['href']
                    else:
                        value = soup_strip_html(cells[1])
        
                    data[key] = value
                
            row_count = row_count + 1
        
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    #sleep for a couple of secs to we don't break anything
    time.sleep(2)
    page = page + 1