###############################################################################
#here is a very hard-coded scrape of Georgia Public Notices
###############################################################################
import mechanize 
import urllib
import cookielib
import time
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki
import lxml.html

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
#print "ok headers"
#list_of_names = []
#list_url = "http://greencracker.net/wp-content/uploads/2012/06/patchsenate.csv"
#response = br.open(list_url)
#html = response.read()
#list_of_names = html.split()
#print list_of_names

names_url = "https://docs.google.com/spreadsheet/pub?key=0AuZMst96R_MYdFdMbGlLbDlDZWJtQmUtSi1paVotU2c&output=html"
key_counter = 0
name_counter = 0
#---- end declarations
names_response = br.open(names_url)
names_html = names_response.read()
names_root = lxml.html.fromstring(names_html)
my_list = []
for td in names_root.cssselect('td.s1'):
    tds = td.cssselect("td")
    their_name = tds[0].text_content()
    my_list.append(their_name)
print "here's how many names:"
my_list = my_list[115:150]  #if want partial list say here
count_of_names = len(my_list)
print count_of_names
base_url = "http://georgiapublicnotice.com"
results_content = "/pages/results_content?"
category = "category=&"

min_date = "min_date=2012-10-01&"
max_date = "max_date=2012-10-30&"
page_label = "page_label=home&"
widget = "widget=search_content&"
string1 = "string=&"
county = "county="

#page_counter = 1
nextpg = """/pages/results_content/push?rel=next&class=next_page&x_page=2&per_page=50&search_content[category]=&search_content[max_date]=&search_content[county]=&search_content[page_label]=results_content&search_content[min_date]=&search_content[phrase_match]=estate&search_content[string]="""


for count_of_names in range(count_of_names):
    print my_list[name_counter]
    print type(my_list[name_counter])
    the_name = (my_list[name_counter])
    print the_name
    print type(the_name)
    the_name = the_name.replace(" ", "+")
    print the_name
    phrase_match = "phrase_match="+the_name+"&"
    url = base_url + results_content + category + phrase_match + min_date + max_date + page_label + widget + string1 + county
    #print br.title()
    #print response.info()
    for pagenum in range (1):
        time.sleep(20)
        response = br.open(url)
        html = response.read()
        print "have searched"
        not_found = re.search("No results found", html)
        if not_found:
            print "but no results found"
            break
        else:
            print "have hits"
            soup = BeautifulSoup(html)
            hits = soup.findAll("a", attrs={"class":"entry-title"})
            count_of_hits = len(hits)
            print "there are this many hits:"
            print count_of_hits
            hit_counter = 0
            print hits[0:count_of_hits]
            for count_of_hits in range (count_of_hits):
                time.sleep(20)
                print "entered loop to iterate hits. here is the contents of hit #"
                print hit_counter
                print hits[hit_counter]
                hit_text = str(hits[hit_counter])
                print "is this text what I need to split?"
                print hit_text
                print "fishing out url-friendly text"
                separated_list = re.split('''"''', hit_text)
                print len(separated_list)
                url_tail = separated_list[1]
                print "about done fishing"
                print url_tail
                print "here's the url of the ad"
                print type(url_tail)
                url = base_url+url_tail               
                response2 = br.open(url)
                print "ad opened success!"
                html = response2.read()
                soup = BeautifulSoup(html)
                print "ad read success! here is its text"
                soup = str(soup)
                name_found = re.search(my_list[name_counter].replace("+", " "), soup)
                print "printing resultof name_found"
                print name_found
                print "have checked in ad for the words: " + my_list[name_counter].replace("+", " ")
                if name_found :
                    print "and found " + my_list[name_counter].replace("+", " ") + " in the ad"
                    data = {
                    'failed' : "",
                    'person' : my_list[name_counter],
                    'text' : hits[hit_counter].contents,
                    'url' : url,
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
                    
                else:
                    print "but did not find " + my_list[name_counter].replace("+", " ") + " in the ad"
                    data = {
                    'failed' : "failed",
                    'person' : my_list[name_counter],
                    'text' : hits[hit_counter].contents,
                    'url' : url,
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
                    
                hit_counter = hit_counter+1
    name_counter = name_counter+1
    #print list_of_names[name_counter]        





    
    ###############################################################################
#here is a very hard-coded scrape of Georgia Public Notices
###############################################################################
import mechanize 
import urllib
import cookielib
import time
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki
import lxml.html

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
#print "ok headers"
#list_of_names = []
#list_url = "http://greencracker.net/wp-content/uploads/2012/06/patchsenate.csv"
#response = br.open(list_url)
#html = response.read()
#list_of_names = html.split()
#print list_of_names

names_url = "https://docs.google.com/spreadsheet/pub?key=0AuZMst96R_MYdFdMbGlLbDlDZWJtQmUtSi1paVotU2c&output=html"
key_counter = 0
name_counter = 0
#---- end declarations
names_response = br.open(names_url)
names_html = names_response.read()
names_root = lxml.html.fromstring(names_html)
my_list = []
for td in names_root.cssselect('td.s1'):
    tds = td.cssselect("td")
    their_name = tds[0].text_content()
    my_list.append(their_name)
print "here's how many names:"
my_list = my_list[115:150]  #if want partial list say here
count_of_names = len(my_list)
print count_of_names
base_url = "http://georgiapublicnotice.com"
results_content = "/pages/results_content?"
category = "category=&"

min_date = "min_date=2012-10-01&"
max_date = "max_date=2012-10-30&"
page_label = "page_label=home&"
widget = "widget=search_content&"
string1 = "string=&"
county = "county="

#page_counter = 1
nextpg = """/pages/results_content/push?rel=next&class=next_page&x_page=2&per_page=50&search_content[category]=&search_content[max_date]=&search_content[county]=&search_content[page_label]=results_content&search_content[min_date]=&search_content[phrase_match]=estate&search_content[string]="""


for count_of_names in range(count_of_names):
    print my_list[name_counter]
    print type(my_list[name_counter])
    the_name = (my_list[name_counter])
    print the_name
    print type(the_name)
    the_name = the_name.replace(" ", "+")
    print the_name
    phrase_match = "phrase_match="+the_name+"&"
    url = base_url + results_content + category + phrase_match + min_date + max_date + page_label + widget + string1 + county
    #print br.title()
    #print response.info()
    for pagenum in range (1):
        time.sleep(20)
        response = br.open(url)
        html = response.read()
        print "have searched"
        not_found = re.search("No results found", html)
        if not_found:
            print "but no results found"
            break
        else:
            print "have hits"
            soup = BeautifulSoup(html)
            hits = soup.findAll("a", attrs={"class":"entry-title"})
            count_of_hits = len(hits)
            print "there are this many hits:"
            print count_of_hits
            hit_counter = 0
            print hits[0:count_of_hits]
            for count_of_hits in range (count_of_hits):
                time.sleep(20)
                print "entered loop to iterate hits. here is the contents of hit #"
                print hit_counter
                print hits[hit_counter]
                hit_text = str(hits[hit_counter])
                print "is this text what I need to split?"
                print hit_text
                print "fishing out url-friendly text"
                separated_list = re.split('''"''', hit_text)
                print len(separated_list)
                url_tail = separated_list[1]
                print "about done fishing"
                print url_tail
                print "here's the url of the ad"
                print type(url_tail)
                url = base_url+url_tail               
                response2 = br.open(url)
                print "ad opened success!"
                html = response2.read()
                soup = BeautifulSoup(html)
                print "ad read success! here is its text"
                soup = str(soup)
                name_found = re.search(my_list[name_counter].replace("+", " "), soup)
                print "printing resultof name_found"
                print name_found
                print "have checked in ad for the words: " + my_list[name_counter].replace("+", " ")
                if name_found :
                    print "and found " + my_list[name_counter].replace("+", " ") + " in the ad"
                    data = {
                    'failed' : "",
                    'person' : my_list[name_counter],
                    'text' : hits[hit_counter].contents,
                    'url' : url,
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
                    
                else:
                    print "but did not find " + my_list[name_counter].replace("+", " ") + " in the ad"
                    data = {
                    'failed' : "failed",
                    'person' : my_list[name_counter],
                    'text' : hits[hit_counter].contents,
                    'url' : url,
                    }
                    scraperwiki.sqlite.save(unique_keys=['url'], data=data)
                    
                hit_counter = hit_counter+1
    name_counter = name_counter+1
    #print list_of_names[name_counter]        





    
    