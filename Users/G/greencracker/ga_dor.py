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

url = "https://etax.dor.ga.gov/TaxExecution/Search.aspx"
names_url = "https://docs.google.com/spreadsheet/pub?key=0AuZMst96R_MYdFdMbGlLbDlDZWJtQmUtSi1paVotU2c&output=html"
key_counter = 0
name_counter = 0
#---- end declarations
names_response = br.open(names_url)
names_html = names_response.read()
print "heres the html of the list of names"
print names_html
names_root = lxml.html.fromstring(names_html)
my_list = []
for td in names_root.cssselect('td.s1'):
    tds = td.cssselect("td")
    their_name = tds[0].text_content()
    my_list.append(their_name)
print "here's how many names:"
print len(my_list)
print "but lets cut that down to"
my_list = my_list[101:200]
count_of_names = len(my_list)

print count_of_names

for name_counter in range (count_of_names):
    response = br.open(url)
    html = response.read()
    print "ok at the search page"
    #print html
    time.sleep(4)
    
    #print "here is the info:"
    #print response.info()

    form = br.select_form(nr=0)
    print "form selected"
    #print type(form)
    
    br.form.set_all_readonly(False)
    
    #print "ok giting post_url"
    post_url, post_data, headers =  br.form.click_request_data()
    #print post_url
    #print post_data
    #print headers
    #print "ok that was the info"

    #for control in br.form.controls: #here's all the controls
    #    print "here is fields and names"
    #    print control.name
    #    print control.value

    eventtarget_control = br.form.find_control("__EVENTTARGET")
    eventargument_control = br.form.find_control("__EVENTARGUMENT")
    viewstate_control = br.form.find_control("__VIEWSTATE")
    eventvalidation_control = br.form.find_control("__EVENTVALIDATION")

    print "here's the name I'm going to put in:"
    print my_list[name_counter]
    br.form['__EVENTTARGET'] = str(eventtarget_control.value)
    br.form['__EVENTARGUMENT'] = str(eventargument_control.value)
    br.form['__VIEWSTATE'] = str(viewstate_control.value)
    br.form['__EVENTVALIDATION'] = str(eventvalidation_control.value)
    br.form['ctl00$ContentPlaceHolderBody$TextBoxTaxpayerNameLike'] = my_list[name_counter]
    #br.form['ct100$ContentPlaceHolderBody$TextBoxTaxpayerDBANameLike'] = ""
    #br.form['ct100$ContentPlaceHolderBody$ListBoxAcctType'] = ""
    #br.form['ctl00$ContentPlaceHolderBody$ListBoxCounty'] = "",
              #'ctl00$ContentPlaceHolderBody$ButtonClear' : '',
              #'ctl00$ContentPlaceHolderBody$ButtonSrch' : '',
    #br.form['ctl00$ctl06'] = '',

    time.sleep(3)
    submit_response = br.submit(name='ctl00$ContentPlaceHolderBody$ButtonSrch')
    html2 = submit_response.read()
    print html2
    print "ok so I submitted that name"

    root = lxml.html.fromstring(html2)
    print "but is that name in there?"
    absent = re.search("No data found for your Search", html2)
    if absent:
        print "no, did not find"
        print my_list[name_counter]
        name_counter = name_counter + 1
        
    else:
        print "found a hit for"
        print my_list[name_counter]
        trs = root.cssselect("tr")
        for td in trs:
                try:
                    print td[1].text_content()
                except IndexError:
                    break
                else:
                    data = {
                    'legal_name' : td[0].text_content(),
                    'dba_name' : td[1].text_content(),
                    'tax_type' :  td[2].text_content(),
                    'lien_number' : td[3].text_content(),
                    'original_lien' : td[4].text_content(),
                    'county' : td[5].text_content(),
                    'date_recorded' : td[6].text_content(),
                    'key' : key_counter
                    }
                    print data
                
                scraperwiki.sqlite.save(unique_keys=['date_recorded'], data=data)
                print "suksesskan!"
    name_counter = name_counter+1