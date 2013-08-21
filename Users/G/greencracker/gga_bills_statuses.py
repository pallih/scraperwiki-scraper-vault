import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
import time
from mechanize import ParseResponse
import urllib
import urllib2
import lxml.html
import re
from lxml import etree

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "ok headers"
#--- end headers
url = "http://www.legis.ga.gov/Legislation/en-US/display/20112012/SR/"
counter = 3
my_list = ["['1']", "['2']", "['3']"]
my_text = ""
my_split = []
bill_number = ""
bill_name = ""
my_str = ""
sponsors_list = []
top_line_list= []
status_list = []
final_result = []
semicolon_list = [" ", ";", " "]
sponsor_1 = ""
sponsor_2 = ""
sponsor_3 = ""
sponsor_4 = ""
sponsor_5 = ""
sponsor_6 = ""
#---- end declarations


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_name_number(soup):
    bill_top_line = soup.findAll('div', {'class' : 'ggah1'})
    for item in bill_top_line:
        bill_number = item.contents[0].encode('ascii', 'ignore')
        bill_name = item.contents[2].encode('ascii', 'ignore')
        top_line_list.append(bill_name)
        top_line_list.append(bill_number)
        #print bill_number
        #print bill_name
    return top_line_list

def get_sponsors(soup):
    sponsors = soup.findAll('span', {'style' : 'float:left; width:33%;'})
    for item in sponsors:
        sponsors_list.append(remove_html_tags((str(item))))
    return sponsors_list
counter = 734
for stuff in range(1373 - counter):    
    top_line_list = []
    sponsors_list = []
    
    my_url = url + str(counter)
    counter = counter + 1
    response = br.open(my_url)
    html = response.read()
    time.sleep(1)
    soup = BeautifulSoup(html)

    get_name_number(soup)
    #print top_line_list
    get_sponsors(soup)
    #print sponsors_list
    top_line_list.append(sponsors_list)
    #print top_line_list
    top_line_list.append(semicolon_list)
    print top_line_list
    data = {
        'bill' : top_line_list
        }

    scraperwiki.sqlite.save(unique_keys=['bill'], data = data)

