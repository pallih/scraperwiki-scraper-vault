import scraperwiki, time, re, mechanize
from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
"""

"""

base_url = 'http://dbh.govt.nz'
first_url = '/market-rent'
http_headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def get_region_data(bs, period):
    br = mechanize.Browser()
    br.addheaders = http_headers
    br.open(base_url + first_url)
    region_btns = bs.findAll('input', {'type':'submit'})
    continue_from  = scraperwiki.sqlite.get_var('last_region_index', 0)
    print "Continuing from: ", continue_from
    region_btns = region_btns[continue_from:-1] # remove totals (last item)
    print region_btns
    for s in region_btns:
        ind = region_btns.index(s)
        scraperwiki.sqlite.save_var('last_region_index', continue_from + ind)
        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        print 'getting region ', s['value']
        # submit
        br.submit(name = s['name'],) # submit each button
        region = s['value'].strip().title()
        # get links
        soup = BeautifulSoup(br.response().read())
        area_submits = soup.findAll('input', {'type':'submit'})
        print area_submits

        for b in area_submits:
            scrape_areas(br, b, period, region)
                
        # send back
        br.back()


def numbers(num):   
    try:
        return int(num)
    except:
        return num

def scrape_areas(br, b, period, region):
        print 'scraping area'
        print b
        district, area = b['value'].split('-', 1)
        # print district + ' ' + area
        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.submit(name = b['name'],) # submit each button

        data_table  =  BeautifulSoup(br.response().read()).\
            findAll('table', {'class':'threedtablecompactmarketrent'})[0]
        print data_table
        headings = [ h.text for h in data_table.findAll('th')]
        print headings

        for r in data_table.findAll('tr'):
            print r
            data_list = [ d.text.replace('$', '') for d in r.findAll('td') ]
            data_list = map(numbers, data_list)
        
            data_dict = dict(zip(headings, data_list))
            
            if data_dict.has_key('Bedrooms'):
                data_dict['Area'] = area.strip()
                data_dict['District'] = district.strip()
                data_dict['Period'] = period['period']
                data_dict['Period_from'] = period['from']
                data_dict['Period_to'] = period['to']
                data_dict['Region'] = region
                # print 'Saving: ', data_dict 
                scraperwiki.datastore.save(unique_keys=['Period', 'Region', 'District', 'Area', 'Dwelling', 'Bedrooms'], data=data_dict)
        # Send Back
        br.back()


def get_period(period_text):
    period = dict()
    period['from'], period['to'] = map(lambda x: x.replace('&nbsp;',' ').strip().title(), re.match('^Market rent &ndash; (.*)-(.*)', period_text).groups())
    # Clean
    period['period']  = "%s to %s" % (period['from'], period['to'])
    period['from'] = time.strptime(period['from'].replace('&nbsp;',' ').strip(), '%d %B %Y')
    period['to'] = time.strptime(period['to'].replace('&nbsp;',' ').strip(), '%d %B %Y')
    # Date please!
    period['from'] = date(period['from'][0],period['from'][1],period['from'][2])
    period['to'] = date(period['to'][0],period['to'][1],period['to'][2])
    return period
    
def Main():
    # scraperwiki.metadata.save('last_region_index', 2)
    html = scraperwiki.scrape(base_url + first_url)
    bs = BeautifulSoup(html)
    period = get_period(bs.find('h1').text)
    get_region_data(bs, period)
    scraperwiki.sqlite.save_var('last_region_index', 0)

Main()import scraperwiki, time, re, mechanize
from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
"""

"""

base_url = 'http://dbh.govt.nz'
first_url = '/market-rent'
http_headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def get_region_data(bs, period):
    br = mechanize.Browser()
    br.addheaders = http_headers
    br.open(base_url + first_url)
    region_btns = bs.findAll('input', {'type':'submit'})
    continue_from  = scraperwiki.sqlite.get_var('last_region_index', 0)
    print "Continuing from: ", continue_from
    region_btns = region_btns[continue_from:-1] # remove totals (last item)
    print region_btns
    for s in region_btns:
        ind = region_btns.index(s)
        scraperwiki.sqlite.save_var('last_region_index', continue_from + ind)
        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        print 'getting region ', s['value']
        # submit
        br.submit(name = s['name'],) # submit each button
        region = s['value'].strip().title()
        # get links
        soup = BeautifulSoup(br.response().read())
        area_submits = soup.findAll('input', {'type':'submit'})
        print area_submits

        for b in area_submits:
            scrape_areas(br, b, period, region)
                
        # send back
        br.back()


def numbers(num):   
    try:
        return int(num)
    except:
        return num

def scrape_areas(br, b, period, region):
        print 'scraping area'
        print b
        district, area = b['value'].split('-', 1)
        # print district + ' ' + area
        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.submit(name = b['name'],) # submit each button

        data_table  =  BeautifulSoup(br.response().read()).\
            findAll('table', {'class':'threedtablecompactmarketrent'})[0]
        print data_table
        headings = [ h.text for h in data_table.findAll('th')]
        print headings

        for r in data_table.findAll('tr'):
            print r
            data_list = [ d.text.replace('$', '') for d in r.findAll('td') ]
            data_list = map(numbers, data_list)
        
            data_dict = dict(zip(headings, data_list))
            
            if data_dict.has_key('Bedrooms'):
                data_dict['Area'] = area.strip()
                data_dict['District'] = district.strip()
                data_dict['Period'] = period['period']
                data_dict['Period_from'] = period['from']
                data_dict['Period_to'] = period['to']
                data_dict['Region'] = region
                # print 'Saving: ', data_dict 
                scraperwiki.datastore.save(unique_keys=['Period', 'Region', 'District', 'Area', 'Dwelling', 'Bedrooms'], data=data_dict)
        # Send Back
        br.back()


def get_period(period_text):
    period = dict()
    period['from'], period['to'] = map(lambda x: x.replace('&nbsp;',' ').strip().title(), re.match('^Market rent &ndash; (.*)-(.*)', period_text).groups())
    # Clean
    period['period']  = "%s to %s" % (period['from'], period['to'])
    period['from'] = time.strptime(period['from'].replace('&nbsp;',' ').strip(), '%d %B %Y')
    period['to'] = time.strptime(period['to'].replace('&nbsp;',' ').strip(), '%d %B %Y')
    # Date please!
    period['from'] = date(period['from'][0],period['from'][1],period['from'][2])
    period['to'] = date(period['to'][0],period['to'][1],period['to'][2])
    return period
    
def Main():
    # scraperwiki.metadata.save('last_region_index', 2)
    html = scraperwiki.scrape(base_url + first_url)
    bs = BeautifulSoup(html)
    period = get_period(bs.find('h1').text)
    get_region_data(bs, period)
    scraperwiki.sqlite.save_var('last_region_index', 0)

Main()