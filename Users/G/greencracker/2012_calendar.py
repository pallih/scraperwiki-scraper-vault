#import re
#import urllib2
#import httplib2
#import urllib
#import cookielib
#import urllib2

#from BeautifulSoup import BeautifulSoup
#cj = cookielib.LWPCookieJar()
#cookie_handler = urllib2.HTTPCookieProcessor(cj)

#http = httplib2.Http()
#base_url = "http://webmail.legis.ga.gov/Calendar/"
#program_url = base_url + "?Chamber=house"
#referer = "http://webmail.legis.ga.gov/Calendar/?chamber=house"
#page = urllib2.urlopen(base_url)
#headers = page.info()

#handler = URL.HTTPBasicAuthHandler()
#opener = URL.build_opener(handler)
#URL.install_opener(opener)

import re
import urllib2

from BeautifulSoup import BeautifulSoup

def main():
    base_url = "http://webmail.legis.ga.gov/Calendar/"
    program_url = base_url + "?Chamber=house"
    html = urllib2.urlopen(program_url).read()
    soup = BeautifulSoup(html)
    
    # Grab all links with __doPostBack in the href attribute
    postback_links = soup.findAll('a', href=re.compile(r'.*?__doPostBack.*'))
    print postback_links
    
    #postback_links now contains a list of anchor entities like below.
    # You can then extract the 'calMain', DDDD arguments from each anchor to build your 
    # POST request for the target event pages that you want to scrape.
    """

    [<a href="javascript:__doPostBack('calMain','4530')" style="color:#999999" title="May 27">27</a>,
     <a href="javascript:__doPostBack('calMain','4531')" style="color:#999999" title="May 28">28</a>,
     <a href="javascript:__doPostBack('calMain','4532')" style="color:#999999" title="May 29">29</a>,
    ...]
    """

if __name__ == '__main__':
    main()

#viewstate ="/wEPDwUJMTExMjM2ODk4D2QWAgIDD2QWAgIBD2QWBGYPZBYCAgEPDxYCHgRUZXh0BQ5Ib3VzZSBNZWV0aW5nc2RkAgEPZBYCAgEPZBYCZg88KwAKAQAPFgQeC1Zpc2libGVEYXRlBgBAbnxE9c4IHgJTRBYBBgBgMk9CE8+IZGRkaK8C5cgvIZSU7yzqs975AQ755fo="
#print viewstate.encode()


#eventvalidation = soup.find('input', id='__EVENTVALIDATION')['value']
#viewstate = soup.find('input', id='__VIEWSTATE')['value']
#formFields = [ 
#                ('__VIEWSTATE',viewstate),
#                ('__EVENTTARGET', 'calMain'),
#                ('__EVENTARGUMENT', 'V4504'),
#                ]
#print formFields

#headers = {
#"Date" : "Fri, 08 Jun 2012 18:34:47 GMT",
#"Server" : "Microsoft-IIS/6.0",
#"X-Powered-By" : "ASP.NET",
#"X-AspNet-Version" : "2.0.50727",
#"Cache-Control" : "private",
#"Content-Type" : "text/html; charset=utf-8",
#"Content-Length" : "12736",
#"User-Agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16",}

#body=urllib.urlencode(formFields)
#print body
#response, content = http.request(program_url, 'POST', headers=headers, body=body)


#headers = {'Cookie': response['set-cookie']}

#response, content = http.request(program_url, 'POST', headers=headers)

#print response

#encodedFields = urllib.urlencode(formFields)
#print encodedFields
#req = urllib2.Request(program_url, encodedFields, headers)
#req.add_header(referer, "http://www.python.org/")

#print req
#print "req ok"
#response = urllib2.urlopen(req)
#print response.read()



#it is a post

#soup = Soup(urlopen(program_url))
#print soup
#print soup.findAll(attrs={'title': 'Go to the previous month'})

#['__EVENTTARGET'] = 'calMain'
#['__EVENTARGUMENT'] = 'V4504'

#br = mechanize.Browser()
#print "ok mechanized"
#br.set_handle_robots(False) 
#print "ok set handle"
# Cookie Jar
#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)

# Browser options
#br.set_handle_equiv(True)
#br.set_handle_gzip(True)
#br.set_handle_redirect(True)
#br.set_handle_referer(True)
#br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
#br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)



#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#print "ok headers"
#response = br.open("http://webmail.legis.ga.gov/Calendar/?Chamber=house")
#print "ok response"
#html = br.response().read()
#print html



#br.select_form(name='Calendar')
#br.form.set_all_readonly(False)
#br['__EVENTTARGET'] = 'calMain'
#br['__EVENTARGUMENT'] = 'V4504'
#response = br.submit()
#html = br.response().read()
#print html


#<form name="Calendar" method="post" action="default.aspx?Chamber=house" id="Calendar">
#<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE"value="/wEPDwUJMTExMjM2ODk4D2QWAgIDD2QWAgIBD2QWBGYPZBYCAgEPDxYCHgRUZXh0BQ5Ib3VzZSBNZWV0aW5nc2RkAgEPZBYCAgEPZBYCZg88KwAKAQAPFgQeC1Zpc2libGVEYXRlBgBgMk9CE8+IHgJTRBYBBgBgMk9CE8+IZGRkIr7yVz8RFKmj71pQiIXgiuCkodM=" />
#<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWLQKm0/PrAgLLwtmvCALKwsHIDwLxkubtCALxkorBAwLxkp66CwLxkqKfAgLxkrbwDQLxktrVBALxku6ODALxkvLjBwLxksaKAgLxkurvDQKUqMT2DgKUqOirBgKUqPyMAQKUqIDgCAKUqJTFAwKUqLi+CwKUqMyTAgKUqND0DQKUqKSfCAKUqMjwAwKrx7rbBAKrx868DAKrx9KRBwKrx+bKDgKrx4quBgKrx56DAQKrx6LkCAKrx7bZAwKrx5rgDgKrx67FCQLO3pisCwLO3qyBAgLO3rD6DQLO3sTfBALO3uiwDALO3vyVBwLO3oDJDgLO3pSiBgLO3vjKBALO3oyuDALl9f62AQLl9YLqCJGRWIFHUkH2uVrXFloomCfGXE87" />





#for link in soup.find_all(attrs={'class': 'cssHeaderCalendarCell'}):
#    print link.get('title').encode("utf-8")," :: ",
#    print "%s%s.rss" % (base_url ,link.get('href'))



#url = 'http://webmail.legis.ga.gov/Calendar/default.aspx'




#longurl = "http://webmail.legis.ga.gov/Calendar/?chamber=house"
#html = urlopen(url).read()
#root = lxml.html.fromstring(html)
#counter = 0
#print html

#string1 = "javascript:__doPostBack('calMain','V4504')"
#string2 = "tbd"
#print html.find(string1)

#soup = BeautifulSoup(html)
#soup = soup.prettify()

#print soup.find_all("a", "cssHeaderCalendarCell")



#for td in root.cssselect("table.tblcHeaderCalendar"):
#    tds = td.cssselect("td")
    
#    data = {
#        'link' : tds[0].text_content(),
#        'link' : tds[1].text_content(),
#        'link' : tds[2].text_content(),
#        }
#    print data



#list1 = re.find(string2, html)
#for counter in range (3):
#    data = {
#    'list1' : list1.index(0),
#    'list2' : list1.index(1),
#    }
#    counter = counter + 1
#print data


#print (html.find(string1))


#<a href="javascript:__doPostBack('calMain','V4504')" style="color:#333333" title="Go to the previous month">May</a>


#thing = urlparse.urlsplit(longurl)
#print thing




          



#soup = BeautifulSoup(html) 



#soup = soup.prettify()


#print soup.find('table')

#html = urlurlopen(url)
#
#print html


#br.select_form(name='Calendar')
    #br.form.set_all_readonly(False)
    #br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    #br['__EVENTARGUMENT'] = ''
    #response = br.submit()


#mnextlink = re.search(""javascript:__doPostBack\('calMain', '4390'"", html") 

    #if not mnextlink:
#        break
    


#mnextlink = re.search("javascript:__doPostBack\('calMain', 4390', html") 
    #if not mnextlink:
    #    break


#br = mechanize.Browser()

    # sometimes the server is sensitive to this information
#
#response = br.open(url)

#for pagenum in range(3):

#print "response ok"
#print response

#html = response.read()
#print html

    #mnextlink = re.search("javascript:__doPostBack\('calMain', 4390', html") 
    #if not mnextlink:
    #    break

    #br.select_form(name='Calendar')
    #br.form.set_all_readonly(False)
    #br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    #br['__EVENTARGUMENT'] = ''
    #response = br.submit()
