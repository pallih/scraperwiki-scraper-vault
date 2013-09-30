import scraperwiki

util = scraperwiki.utils.swimport("utility_library")
scrape_lib = scraperwiki.utils.swimport("pa_scraper_library")

def run(test_query = None):
    try:
        query = scraperwiki.utils.GET()
    except:
        query = {}
    if 'test' in query: 
        scrape_lib.debug = True # verbose
        if test_query:
            query = test_query
    fmt = query.get('fmt', '')
    if not fmt or fmt == 'rss' or fmt == 'atom' or fmt == 'object':
        fmt = 'xml'
    query['fmt'] = 'object'
    result = scrape_lib.execute_scrape(query)
    
    if 'redirect' in query and 'ref' in query:
        try:
            if int(result['count']) == 1:
                applications = result['applications']['application']
                url = result['applications']['application'][0]['info_url']
            else:
                raise Exception()
        except:
            query['fmt'] = fmt
            util.set_content(fmt)
            print scrape_lib.show_data(result, query)
        else:
            util.redirect(url)
    else:
        query['fmt'] = fmt
        util.set_content(fmt)
        print scrape_lib.show_data(result, query)

#from datetime import datetime
#print datetime.fromtimestamp(1341705600)
#sys.exit()

# for testing if the real query is set to 'test=any_value', it is replaced by the test query defined below
test_query = { 'fmt': 'xml' }
#test_query = { 'date': '08/06/2012', 'ndays': '14', 'no_detail': 'true' } 
#test_query = { 'ref': 'P/2011/1170' } 
test_query = { 'day': '06', 'month': '05', 'year': '2013', 'fmt': 'xml', 'ndays': '-14' } 
#test_query = { 'day': '6', 'month': '8', 'year': '2011' } # weekend so should return empty but valid response
test_query['auth'] = "South Hams"

run(test_query)



import scraperwiki

util = scraperwiki.utils.swimport("utility_library")
scrape_lib = scraperwiki.utils.swimport("pa_scraper_library")

def run(test_query = None):
    try:
        query = scraperwiki.utils.GET()
    except:
        query = {}
    if 'test' in query: 
        scrape_lib.debug = True # verbose
        if test_query:
            query = test_query
    fmt = query.get('fmt', '')
    if not fmt or fmt == 'rss' or fmt == 'atom' or fmt == 'object':
        fmt = 'xml'
    query['fmt'] = 'object'
    result = scrape_lib.execute_scrape(query)
    
    if 'redirect' in query and 'ref' in query:
        try:
            if int(result['count']) == 1:
                applications = result['applications']['application']
                url = result['applications']['application'][0]['info_url']
            else:
                raise Exception()
        except:
            query['fmt'] = fmt
            util.set_content(fmt)
            print scrape_lib.show_data(result, query)
        else:
            util.redirect(url)
    else:
        query['fmt'] = fmt
        util.set_content(fmt)
        print scrape_lib.show_data(result, query)

#from datetime import datetime
#print datetime.fromtimestamp(1341705600)
#sys.exit()

# for testing if the real query is set to 'test=any_value', it is replaced by the test query defined below
test_query = { 'fmt': 'xml' }
#test_query = { 'date': '08/06/2012', 'ndays': '14', 'no_detail': 'true' } 
#test_query = { 'ref': 'P/2011/1170' } 
test_query = { 'day': '06', 'month': '05', 'year': '2013', 'fmt': 'xml', 'ndays': '-14' } 
#test_query = { 'day': '6', 'month': '8', 'year': '2011' } # weekend so should return empty but valid response
test_query['auth'] = "South Hams"

run(test_query)



