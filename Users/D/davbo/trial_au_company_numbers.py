import urllib2, urllib
try:
    import scraperwiki
except:
    pass
from lxml import html

abns = []

def scrape_page(src):
    root = html.fromstring(src)
    trs = root.cssselect('tr')
    results = []
    for tr in trs:
        tds = tr.cssselect('td')
        if len(tds) == 4:
            abn = tds[0].cssselect('a')[0].text
            status = tds[0].text_content().strip().lstrip(abn)
            abn = abn.encode('latin-1').replace('\xa0',' ')
            if abn in abns:
                print "DUPLICATE"
                continue
            else:
                abns.append(abn)
            name = tds[1].cssselect('span')[0].text
            name_type = ts[2].text_content()
            location = "%s %s" % tuple((tds[3].text.strip().split()))
            results.append({'CompanyNumber':abn, 'Status':status, 'CompanyName':name, 'NameType':name_type, 'CompanyAddress':location})
    next_link = dict(root.get_element_by_id('_ctl0_TopNextPageLink').items())
    if 'href' in next_link:
        return results, "http://www.abr.business.gov.au/"+next_link['href']
    else:
        return results, False


abc = "abcdefghijklmnopqrstuvwxyz"
total_results = []
count = 0
try:
    starting_point = scraperwiki.sqlite.get_var('starting_point', default='aa')
    starting_state = scraperwiki.sqlite.get_var('starting_state', default='ACT')
    scraperwiki.sqlite.save_var('data_columns', ['CompanyNumber', 'CompanyName', 'NameType', 'Status', 'CompanyAddress'])
except:
    starting_point = 'aaa'
    starting_state = 'ACT'
running = False
states = ['ACT', 'NSW' 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
for state in states:
    if not running and state != starting_state:
        continue
    state_qstr = ['0,','0,','0,','0,','0,','0,','0,','0,']
    state_qstr[states.index(state)] = '1,'
    scraperwiki.sqlite.save_var('starting_state', state)
    for letter in abc:
        if not running and letter != starting_point[0]:
            continue
        for letter2 in abc:
            if not running and letter2 != starting_point[1]:
                continue
            for letter3 in abc:
                        if not running and letter3 != starting_point[2]:
                            continue
                        running = True
                        params = urllib.urlencode(({'SearchText': urllib.quote(letter+letter2),'StateOptions': urllib.quote("".join(state_qstr)),'Postcode': "ALL",'NameOptions': urllib.quote("1,0,0,0,0,0") ,'SearchWidth': "" ,'MaxResults': "0" }))
                                
                               
                        urls = ["http://www.abr.business.gov.au/SearchByName.aspx?%s" % (params)]
                        while urls:
                             count += 1
                             url = urls.pop()
                             next_url = False
                             try:
                                 response = urllib2.urlopen(url)
                                 page_results, next_url = scrape_page(response.read())
                                 total_results += page_results
                                 for r in page_results:
                                    scraperwiki.sqlite.save_var(['CompanyNumber'], r)
                                    scraperwiki.sqlite.save_var('starting_point', letter+letter2)
                             except:
                                 pass
                
                             if next_url:
                                 urls.append(next_url)
                                 print "Got next url: ", next_url, count
                             print "Parsed page: ", url, count

# if finished all letters and states without interruption then reset
starting_point = 'aaa'
starting_state = 'ACT'
scraperwiki.sqlite.save_var('starting_state', state)
scraperwiki.sqlite.save_var('starting_point', starting_point)