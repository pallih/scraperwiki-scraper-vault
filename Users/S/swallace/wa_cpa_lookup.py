#
# How to use:
# 1) enter the desired city
# 2) find out manually how many pages there are for the results, enter
# note: you can also find all in Japan by entering JAPAN in the country field and leaving the city field blank

import scraperwiki
import requests
import lxml.html

SEARCH_CITY = "seattle"
PAGES = 5
STARTURL = 'http://www.cpaboard.wa.gov/LicenseeSearchApp/'

#######################
###     methods     ###
#######################


def print_results(html):
    """
    prints the results of the browser
    """
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr")[1:-2]:
        tds = tr.cssselect("td")
        data = { 'fname' : tds[0].text_content(),
                 'lname' : tds[2].text_content(),
                 'city'  : tds[3].text_content(),
                 'lic_num': tds[6].text_content(),
                 'orig'  : tds[7].text_content(),
                 'exp'   : tds[8].text_content()
                }
        print data

def save_results(html):
    """
    saves the results of the browser
    """
    root = lxml.html.fromstring(html)
    
    #if theres only 1 page, need to pull from second row to end, else need to exclude the last row which is used for pages
    if PAGES == 1:
        for tr in root.cssselect("tr")[1:]:
            tds = tr.cssselect("td")
            data = { 'fname' : tds[0].text_content(),
                     'lname' : tds[2].text_content(),
                     'city'  : tds[3].text_content(),
                     'lic_num': tds[6].text_content(),
                     'orig'  : tds[7].text_content(),
                     'exp'   : tds[8].text_content()
                    }
            scraperwiki.sqlite.save(unique_keys=['lic_num'], data=data)
    else:
        for tr in root.cssselect("tr")[1:-2]:
            tds = tr.cssselect("td")
            data = { 'fname' : tds[0].text_content(),
                     'lname' : tds[2].text_content(),
                     'city'  : tds[3].text_content(),
                     'lic_num': tds[6].text_content(),
                     'orig'  : tds[7].text_content(),
                     'exp'   : tds[8].text_content()
                    }
            scraperwiki.sqlite.save(unique_keys=['lic_num'], data=data)
        
        
def load_payload(html, page_num):
    """
    gets the two values needed to advance to other pages
    then loads the payload and returns it
    """
    
    #the first page doesn't need a value
    #test this out once
    #
    #
    if page_num == 1:
        page_var = ""
    else:
        page_var = 'Page$' + str(page_num)
        
    root = lxml.html.fromstring(html)
    
    #pick up the javascript values
    EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value']
    #find the __EVENTVALIDATION value
    VIEWSTATE = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    #find the __VIEWSTATE value

    payload = {'__EVENTTARGET': '_gridViewCpa',
    '__EVENTARGUMENT':page_var,
    '__LASTFOCUS':'',
    '__VIEWSTATE':VIEWSTATE,
    '__EVENTVALIDATION':EVENTVALIDATION,
    '_txtFirstName':'',
    '_txtLastName':'',
    '_txtCert':'',
    '_ddlCountry':'',
    '_txtCity':SEARCH_CITY,
    '_ddlState':'',
    '_btnSearch':'',
    '_btnClear':'',
    '_btnSwitchView':''
    }
    
    #need to remove the buttons for all pages except the first page
    if page_num != 1:
        payload.pop("_btnSearch")
        payload.pop("_btnClear")
        payload.pop("_btnSwitchView")

    return payload

    
#######################
##   Start program   ##
#######################

s = requests.session()
r0 = s.get(STARTURL)


#load the payload from the current page
#post using the payload
#save results
payload = load_payload(r0.text, 1)
results_page = s.post(STARTURL, data=payload)
save_results(results_page.text)

for i in range(2,pages + 1):
    payload = load_payload(results_page.text, i)
    results_page = s.post(STARTURL, data=payload)
    save_results(results_page.text)
