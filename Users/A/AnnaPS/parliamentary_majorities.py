import scraperwiki
import lxml.html
import urllib

DOMAIN = 'http://www.parliament.uk'
ALL_MPS = '%s%s' % (DOMAIN, '/mps-lords-and-offices/mps/')

html = scraperwiki.scrape(ALL_MPS)
print html
root = lxml.html.fromstring(html.decode('utf8')) 
mp_table = root.cssselect('table')[1]
mp_rows = mp_table.cssselect('tbody tr')
for mp_row in mp_rows:
    data = {}
    mp_cells = mp_row.cssselect("td")
    if len(mp_cells) > 1:
        mp_a = mp_cells[0].cssselect("a")[0]
        data['party'] = mp_a.tail.strip().replace('(','').replace(')','')
        mp_name_original = mp_a.text
        #if mp_name_original != 'Coffey, Thérèse':
        #    continue
        mp_names = mp_name_original.split(', ')
        data['mp_name'] = '%s %s' % (mp_names[1], mp_names[0])
        mp_url = mp_a.get('href')
        data['mp_id'] = mp_url.split('/')[-1]
        data['mp_url'] = '%s%s' % (DOMAIN, urllib.quote(mp_url.encode('utf8')))
        data['constituency'] = mp_cells[1].text
        html = scraperwiki.scrape(data['mp_url'])
        root = lxml.html.fromstring(html.decode('utf8'))
        results_rows = root.cssselect('table tbody tr')
        mp_result = results_rows[0].cssselect('td')
        data['mp_vote'] = mp_result[2].text
        data['mp_percentage'] = mp_result[3].text
        footer_cells = root.cssselect('table tbody tr td.footer')
        data['majority_raw'] = footer_cells[2].text
        data['majority_percent'] = footer_cells[3].text
        data['turnout_raw'] = footer_cells[6].text
        print data
        scraperwiki.sqlite.save(['mp_id'], data)
        import scraperwiki
import lxml.html
import urllib

DOMAIN = 'http://www.parliament.uk'
ALL_MPS = '%s%s' % (DOMAIN, '/mps-lords-and-offices/mps/')

html = scraperwiki.scrape(ALL_MPS)
print html
root = lxml.html.fromstring(html.decode('utf8')) 
mp_table = root.cssselect('table')[1]
mp_rows = mp_table.cssselect('tbody tr')
for mp_row in mp_rows:
    data = {}
    mp_cells = mp_row.cssselect("td")
    if len(mp_cells) > 1:
        mp_a = mp_cells[0].cssselect("a")[0]
        data['party'] = mp_a.tail.strip().replace('(','').replace(')','')
        mp_name_original = mp_a.text
        #if mp_name_original != 'Coffey, Thérèse':
        #    continue
        mp_names = mp_name_original.split(', ')
        data['mp_name'] = '%s %s' % (mp_names[1], mp_names[0])
        mp_url = mp_a.get('href')
        data['mp_id'] = mp_url.split('/')[-1]
        data['mp_url'] = '%s%s' % (DOMAIN, urllib.quote(mp_url.encode('utf8')))
        data['constituency'] = mp_cells[1].text
        html = scraperwiki.scrape(data['mp_url'])
        root = lxml.html.fromstring(html.decode('utf8'))
        results_rows = root.cssselect('table tbody tr')
        mp_result = results_rows[0].cssselect('td')
        data['mp_vote'] = mp_result[2].text
        data['mp_percentage'] = mp_result[3].text
        footer_cells = root.cssselect('table tbody tr td.footer')
        data['majority_raw'] = footer_cells[2].text
        data['majority_percent'] = footer_cells[3].text
        data['turnout_raw'] = footer_cells[6].text
        print data
        scraperwiki.sqlite.save(['mp_id'], data)
        