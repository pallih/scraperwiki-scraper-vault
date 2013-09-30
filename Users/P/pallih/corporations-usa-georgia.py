# -*- coding: utf-8 -*


#opencorporates georgia -- usa

import scraperwiki,re
#from lxml import etree
import lxml.html
import urllib2

#first page:
# http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&FormName=CorpNameSearch

#second page:
#http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec=0&FormName=CorpNameSearch&Pos=Next+50+%3E%3E

#third page:
#http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec=50&FormName=CorpNameSearch&Pos=Next+50+%3E%3E

# + 50 each time for TopRec



#Runtime info setup:
#record = {}
#record ['lastTopRec'] = '0'
#scraperwiki.sqlite.save(['lastTopRec'], data=record, table_name='runtime_info')
#exit()

regex = re.compile("Next 50")

def scrape(last_int):
    if last_int == '0':
        print 'get first page'
    
    #html = scraperwiki.scrape('http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec='+str(last_int)+'&FormName=CorpNameSearch&Pos=Next+50+%3E%3E')
    try:
        resp = urllib2.urlopen('http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=%&TopRec='+str(last_int)+'&FormName=CorpNameSearch&Pos=Next+50+%3E%3E')
        html = resp.read()
    except urllib2.HTTPError, error:
        print 'The server could  not fulfill the request.'
        print 'Error code: ', error.code
    #except URLError, error:
    #    print 'We failed to reach a server.'
    #    print 'Reason: ', error.reason
    root = lxml.html.fromstring(html)
    
    results = root.xpath('//table//table//table//tr')
    #print len(results)
    #print results
    for tr in results[6:]:
        record = {}
        record['name'] = tr[0].text_content()
        record['detail_url'] = 'http://corp.sos.state.ga.us/corp/soskb/' + tr[0][0][0].get('href')
        record['control_no'] = tr[1].text_content()
        record['type'] = tr[2].text_content()
        record['status'] = tr[3].text_content()
        record['creation_date'] = tr[4].text_content()
        scraperwiki.sqlite.save(['name', 'control_no'], data=record, table_name='us_georgia_corporate_entities')
    update_statement= 'update runtime_info SET lastTopRec=' + str(last_int)
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    if regex.findall(html):
        #print 'there is a next page'
        next_int = int(last_int)+50
        print 'get results: ', next_int, '-', next_int+50
        #time.sleep(2) #sleep for 2 sec - a desperate attempt to avoid 500 errors from the server
        scrape(next_int)   

selection_statement = '* from runtime_info'
last_done = scraperwiki.sqlite.select(selection_statement)
for last in last_done:
    last_int = last['lastTopRec']
print 'Last done: ',last_int
scrape(last_int)


# -*- coding: utf-8 -*


#opencorporates georgia -- usa

import scraperwiki,re
#from lxml import etree
import lxml.html
import urllib2

#first page:
# http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&FormName=CorpNameSearch

#second page:
#http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec=0&FormName=CorpNameSearch&Pos=Next+50+%3E%3E

#third page:
#http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec=50&FormName=CorpNameSearch&Pos=Next+50+%3E%3E

# + 50 each time for TopRec



#Runtime info setup:
#record = {}
#record ['lastTopRec'] = '0'
#scraperwiki.sqlite.save(['lastTopRec'], data=record, table_name='runtime_info')
#exit()

regex = re.compile("Next 50")

def scrape(last_int):
    if last_int == '0':
        print 'get first page'
    
    #html = scraperwiki.scrape('http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=*&TopRec='+str(last_int)+'&FormName=CorpNameSearch&Pos=Next+50+%3E%3E')
    try:
        resp = urllib2.urlopen('http://corp.sos.state.ga.us/corp/soskb/searchresults.asp?Words=Starting&searchstr=%&TopRec='+str(last_int)+'&FormName=CorpNameSearch&Pos=Next+50+%3E%3E')
        html = resp.read()
    except urllib2.HTTPError, error:
        print 'The server could  not fulfill the request.'
        print 'Error code: ', error.code
    #except URLError, error:
    #    print 'We failed to reach a server.'
    #    print 'Reason: ', error.reason
    root = lxml.html.fromstring(html)
    
    results = root.xpath('//table//table//table//tr')
    #print len(results)
    #print results
    for tr in results[6:]:
        record = {}
        record['name'] = tr[0].text_content()
        record['detail_url'] = 'http://corp.sos.state.ga.us/corp/soskb/' + tr[0][0][0].get('href')
        record['control_no'] = tr[1].text_content()
        record['type'] = tr[2].text_content()
        record['status'] = tr[3].text_content()
        record['creation_date'] = tr[4].text_content()
        scraperwiki.sqlite.save(['name', 'control_no'], data=record, table_name='us_georgia_corporate_entities')
    update_statement= 'update runtime_info SET lastTopRec=' + str(last_int)
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    if regex.findall(html):
        #print 'there is a next page'
        next_int = int(last_int)+50
        print 'get results: ', next_int, '-', next_int+50
        #time.sleep(2) #sleep for 2 sec - a desperate attempt to avoid 500 errors from the server
        scrape(next_int)   

selection_statement = '* from runtime_info'
last_done = scraperwiki.sqlite.select(selection_statement)
for last in last_done:
    last_int = last['lastTopRec']
print 'Last done: ',last_int
scrape(last_int)


