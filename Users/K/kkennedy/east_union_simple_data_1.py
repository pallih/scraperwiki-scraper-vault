import scraperwiki,requests,lxml.html

# Blank Python

scrape_continue= True
schoolcodes = ['308']
years = ["2010-2011","2009-2010"]
#scraperwiki.sqlite.save_var('next_year', "2001-2002") 

starturl = 'http://www.ncreportcard.org/src/main.jsp?pList=2&pYear=2010-2011'

def yearscrape():
    data = []
    y_url="http://www.ncreportcard.org/src/"
    html = scraperwiki.scrape(y_url)
    root = lxml.html.fromstring(html)
    working = root.xpath("/html//option")
    for rawdata in working:
        if rawdata.get("value").startswith("main.jsp?pYear"):
            data.append(rawdata.text_content())
            #data.append(rawdata.get("value"))
            print rawdata.get("value"), rawdata.text_content()
    print data
    print len(data)
    for row in data:
        highyear = row.split('-')
        print row
        print int(highyear[0])

    maxyear = max(x.split('-')[0] for x in data)
    print maxyear

def basescrape():
    data = []
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    working = root.xpath("/html//option")
    for rawdata in working:
        if not rawdata.get("value").startswith("main.jsp?pYear"):
            data.append(rawdata.get("value"))
            print rawdata.get("value"), rawdata.text_content()
        # data[raw
    print data
    print len(data)

def url2url(url):
    return "http://www.ncreportcards.org/src/search.jsp?pYear=%s" % (url,)

def scrapeurl(url):
    html=requests.get(url).content
    myteam=lxml.html.fromstring(html).get_element_by_id('my-teams-table')
    prev=myteam.cssselect('strong a')[0]
    previous=prev.attrib['href']
    try:
        assert prev.text_content().strip()=='Previous Games' # watch for termination
    except:
        previous=None
    for row in myteam.cssselect("tr td[align='center']"):
        if row.text_content().strip() == "Score":
            continue
        data={'url':row.cssselect("a")[0].attrib['href']}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name='prem-walker')
    scraperwiki.sqlite.save_var('nexturl', previous)
    return previous

#starturl='http://soccernet.espn.go.com/results/_/league/eng.1/barclays-premier-league'

baseurl=scraperwiki.sqlite.get_var('next_year')

# check years
# check schools/year

while scrape_continue:
    
    yearscrape()
    ##basescrape()
    ###u=url2url(baseurl)
    ###print u
    #scrapeurl(u)
    #baseurl=nexturl(baseurl)
    #scraperwiki.sqlite.save_var('next',baseurl)
    scrape_continue = False

#print data
#html = scraperwiki.scrape("http://www.ncreportcard.org/src/schDetails.jsp?Page=4&pSchCode=308&pLEACode=900&pYear=2010-2011")
#print html



#import lxml.html 
#import lxml.etree           
#root = lxml.html.fromstring(html)
#tbl = root.xpath("/html//table")
#for t in tbl:
#    if t.get("summary") is not None and t.get("summary").startswith("The total number of classroom teachers"):
#        tds = t.cssselect("td")
#        print tds
#        data = {
#                'classroom_teachers' : tds[1].text_content(),
#                #'classroom_teachers' : int(tds[1].text_content()),
#                'district_avg_ct' : int(tds[2].text_content()),
#                'state_avg_ct': int(tds[3].text_content())
#        }
#        #for tr in tds:
#        #    data = {
#        #        'classroom_teachers' : tds[1].text_content(),
#        #        #'classroom_teachers' : int(tds[1].text_content()),
#        #        'district_avg' : int(tds[2].text_content()),
#        #        'state_avg': int(tds[3].text_content())
#        #    }
#            #print tr.text_content()
#        #print data

        #print lxml.etree.tostring(t)
#    if t.get("summary") is not None and t.get("summary").startswith("The number of school staff, including teachers"):
#        tds = t.cssselect("td")
#        scratch = [ tr.text_content() for tr in tds ]
#        #print scratch
#        data['nat_board_teachers'] = tds[1].text_content()
#        data['district_avg_nb'] = tds[1].text_content()
#        data['state_avg_nb'] = tds[1].text_content()
#        #print lxml.etree.tostring(t)

import scraperwiki,requests,lxml.html

# Blank Python

scrape_continue= True
schoolcodes = ['308']
years = ["2010-2011","2009-2010"]
#scraperwiki.sqlite.save_var('next_year', "2001-2002") 

starturl = 'http://www.ncreportcard.org/src/main.jsp?pList=2&pYear=2010-2011'

def yearscrape():
    data = []
    y_url="http://www.ncreportcard.org/src/"
    html = scraperwiki.scrape(y_url)
    root = lxml.html.fromstring(html)
    working = root.xpath("/html//option")
    for rawdata in working:
        if rawdata.get("value").startswith("main.jsp?pYear"):
            data.append(rawdata.text_content())
            #data.append(rawdata.get("value"))
            print rawdata.get("value"), rawdata.text_content()
    print data
    print len(data)
    for row in data:
        highyear = row.split('-')
        print row
        print int(highyear[0])

    maxyear = max(x.split('-')[0] for x in data)
    print maxyear

def basescrape():
    data = []
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    working = root.xpath("/html//option")
    for rawdata in working:
        if not rawdata.get("value").startswith("main.jsp?pYear"):
            data.append(rawdata.get("value"))
            print rawdata.get("value"), rawdata.text_content()
        # data[raw
    print data
    print len(data)

def url2url(url):
    return "http://www.ncreportcards.org/src/search.jsp?pYear=%s" % (url,)

def scrapeurl(url):
    html=requests.get(url).content
    myteam=lxml.html.fromstring(html).get_element_by_id('my-teams-table')
    prev=myteam.cssselect('strong a')[0]
    previous=prev.attrib['href']
    try:
        assert prev.text_content().strip()=='Previous Games' # watch for termination
    except:
        previous=None
    for row in myteam.cssselect("tr td[align='center']"):
        if row.text_content().strip() == "Score":
            continue
        data={'url':row.cssselect("a")[0].attrib['href']}
        scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name='prem-walker')
    scraperwiki.sqlite.save_var('nexturl', previous)
    return previous

#starturl='http://soccernet.espn.go.com/results/_/league/eng.1/barclays-premier-league'

baseurl=scraperwiki.sqlite.get_var('next_year')

# check years
# check schools/year

while scrape_continue:
    
    yearscrape()
    ##basescrape()
    ###u=url2url(baseurl)
    ###print u
    #scrapeurl(u)
    #baseurl=nexturl(baseurl)
    #scraperwiki.sqlite.save_var('next',baseurl)
    scrape_continue = False

#print data
#html = scraperwiki.scrape("http://www.ncreportcard.org/src/schDetails.jsp?Page=4&pSchCode=308&pLEACode=900&pYear=2010-2011")
#print html



#import lxml.html 
#import lxml.etree           
#root = lxml.html.fromstring(html)
#tbl = root.xpath("/html//table")
#for t in tbl:
#    if t.get("summary") is not None and t.get("summary").startswith("The total number of classroom teachers"):
#        tds = t.cssselect("td")
#        print tds
#        data = {
#                'classroom_teachers' : tds[1].text_content(),
#                #'classroom_teachers' : int(tds[1].text_content()),
#                'district_avg_ct' : int(tds[2].text_content()),
#                'state_avg_ct': int(tds[3].text_content())
#        }
#        #for tr in tds:
#        #    data = {
#        #        'classroom_teachers' : tds[1].text_content(),
#        #        #'classroom_teachers' : int(tds[1].text_content()),
#        #        'district_avg' : int(tds[2].text_content()),
#        #        'state_avg': int(tds[3].text_content())
#        #    }
#            #print tr.text_content()
#        #print data

        #print lxml.etree.tostring(t)
#    if t.get("summary") is not None and t.get("summary").startswith("The number of school staff, including teachers"):
#        tds = t.cssselect("td")
#        scratch = [ tr.text_content() for tr in tds ]
#        #print scratch
#        data['nat_board_teachers'] = tds[1].text_content()
#        data['district_avg_nb'] = tds[1].text_content()
#        data['state_avg_nb'] = tds[1].text_content()
#        #print lxml.etree.tostring(t)

