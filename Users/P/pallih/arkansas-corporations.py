# -*- coding: utf-8 -*


#opencorporates arkansas

import scraperwiki,re
#from lxml import etree
import lxml.html
import time
import datetime
import urllib2

url = 'http://www.sos.arkansas.gov/corps/search_all.php'

# http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run=1360&corp_type_id=&corp_name=&agent_search=&agent_city=&agent_state=AR&filing_number=&cmd=

# http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run=0&corp_type_id=&corp_name=&agent_search=&agent_city=&agent_state=AR&filing_number=&cmd=

#http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&agent_state=AR&run=0

## {{{ http://code.activestate.com/recipes/577305/ (r1)
states = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}
## end of http://code.activestate.com/recipes/577305/ }}}

def start_again():
    #drop runtime_info table to start again
    scraperwiki.sqlite.execute("drop table if exists runtime_info")

    #Runtime info setup:
    for k, v in states.iteritems():
        record = {}
        record ['state'] = v
        record ['code'] = k
        record ['last_page'] = 0
        record ['done'] = 0    
        print record
        scraperwiki.sqlite.save(['code'], data=record, table_name='runtime_info')
    run()


def scrape(state,page):
    url = 'http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run='+str(page)+'&agent_state='+state+'&corp_type_id=&corp_name=&agent_search=&agent_city=&filing_number=&cmd='
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #td valign="top"class="light"
    results = root.xpath('//td[@class="light" or @class="alt"]/..')
    if results:
        print 'processing results for ' + str(state) + ' page ' + str(page)
        for m in results:
            record = {}
            record['name'] = m[0].text_content()
            record['detail_url'] = 'http://www.sos.arkansas.gov/corps/' + m[0][0][0][0].get('href')
            record['city'] = m[1].text_content()
            record['state'] = m[2].text_content()
            record['status'] =m[3].text_content()
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
            scraperwiki.sqlite.save(['name', 'city', 'state'], data=record, table_name='us_arkansas_corporate_entities')
        next = root.xpath('//a[text()="Next 250 >>"]')
        if next:
            print "there are more results - let's process (last page done was: " + str(page) + " of state: "+ state +" )"
            # update last page done
            update_statement= 'update runtime_info SET last_page=' + str(page) + ' WHERE code='+ '"' + state+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            page = int(page)+1
            # scrape next page
            scrape(state,page)
        else:
            print 'Last page of results - Done with state: ' + state
            #update last page and done field
            update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE code='+ '"' + state+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
    else:
        print 'No results - Done with state: ' + state
        # update last page and done field
        update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE code='+ '"' + state+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()

def run():
    for states in states_todo:
        state=states['code']
        page=states['last_page']
        scrape(state,page)    

selection_statement = '* from runtime_info where done=0'
states_todo = scraperwiki.sqlite.select(selection_statement)

if states_todo:
    todo_list = []
    for states in states_todo:
        state=states['state']
        todo_list.append(state) 
    #print ",".join(str(states_todo)
    print 'there are states left to do ('+ str(todo_list) + ')'
    run()

else:
    print 'there are no states left to do - now we drop the runtime_info table and start again'
    start_again()
    run()
    




# -*- coding: utf-8 -*


#opencorporates arkansas

import scraperwiki,re
#from lxml import etree
import lxml.html
import time
import datetime
import urllib2

url = 'http://www.sos.arkansas.gov/corps/search_all.php'

# http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run=1360&corp_type_id=&corp_name=&agent_search=&agent_city=&agent_state=AR&filing_number=&cmd=

# http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run=0&corp_type_id=&corp_name=&agent_search=&agent_city=&agent_state=AR&filing_number=&cmd=

#http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&agent_state=AR&run=0

## {{{ http://code.activestate.com/recipes/577305/ (r1)
states = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}
## end of http://code.activestate.com/recipes/577305/ }}}

def start_again():
    #drop runtime_info table to start again
    scraperwiki.sqlite.execute("drop table if exists runtime_info")

    #Runtime info setup:
    for k, v in states.iteritems():
        record = {}
        record ['state'] = v
        record ['code'] = k
        record ['last_page'] = 0
        record ['done'] = 0    
        print record
        scraperwiki.sqlite.save(['code'], data=record, table_name='runtime_info')
    run()


def scrape(state,page):
    url = 'http://www.sos.arkansas.gov/corps/search_corps.php?SEARCH=1&run='+str(page)+'&agent_state='+state+'&corp_type_id=&corp_name=&agent_search=&agent_city=&filing_number=&cmd='
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #td valign="top"class="light"
    results = root.xpath('//td[@class="light" or @class="alt"]/..')
    if results:
        print 'processing results for ' + str(state) + ' page ' + str(page)
        for m in results:
            record = {}
            record['name'] = m[0].text_content()
            record['detail_url'] = 'http://www.sos.arkansas.gov/corps/' + m[0][0][0][0].get('href')
            record['city'] = m[1].text_content()
            record['state'] = m[2].text_content()
            record['status'] =m[3].text_content()
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
            scraperwiki.sqlite.save(['name', 'city', 'state'], data=record, table_name='us_arkansas_corporate_entities')
        next = root.xpath('//a[text()="Next 250 >>"]')
        if next:
            print "there are more results - let's process (last page done was: " + str(page) + " of state: "+ state +" )"
            # update last page done
            update_statement= 'update runtime_info SET last_page=' + str(page) + ' WHERE code='+ '"' + state+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            page = int(page)+1
            # scrape next page
            scrape(state,page)
        else:
            print 'Last page of results - Done with state: ' + state
            #update last page and done field
            update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE code='+ '"' + state+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
    else:
        print 'No results - Done with state: ' + state
        # update last page and done field
        update_statement= 'update runtime_info SET last_page=' + str(page) + ', done=1 WHERE code='+ '"' + state+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()

def run():
    for states in states_todo:
        state=states['code']
        page=states['last_page']
        scrape(state,page)    

selection_statement = '* from runtime_info where done=0'
states_todo = scraperwiki.sqlite.select(selection_statement)

if states_todo:
    todo_list = []
    for states in states_todo:
        state=states['state']
        todo_list.append(state) 
    #print ",".join(str(states_todo)
    print 'there are states left to do ('+ str(todo_list) + ')'
    run()

else:
    print 'there are no states left to do - now we drop the runtime_info table and start again'
    start_again()
    run()
    




