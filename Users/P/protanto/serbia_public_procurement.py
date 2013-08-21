import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector

URL = 'http://portal.ujn.gov.rs'
URL = 'http://portal.ujn.gov.rs/Izvestaji.aspx'
AGENT = 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11'
HEADERS = {
    #'User-agent': AGENT,
}
POSTHEADERS = {
    #'User-agent': AGENT,
    #'Content-Type':'application/x-www-form-urlencoded',
    #'Host': 'portal.ujn.gov.rs',
    #'Origin': 'http://portal.ujn.gov.rs',
    'Referer': 'http://portal.ujn.gov.rs/Izvestaji.aspx',
}
FORM_DATA = {
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder3$grwIzvestaji',
    '__VIEWSTATEENCRYPTED': '',
    'ctl00$txtUser':'',
    'ctl00$txtPass':'',
    'ctl00$ContentPlaceHolder1$txtSearchIzvestaj':'',
    #'referer':'http://portal.ujn.gov.rs/Izvestaji.aspx',
}



def parse_html(html):
    table = html.get_element_by_id('ctl00_ContentPlaceHolder3_grwIzvestaji')
    rows = iter(table)
    rows.next()
    for row in rows:
        yield row.text_content()
        

def main():
    i = 0
    #home = requests.get(URL)
    #cookies = requests.utils.dict_from_cookiejar(home.cookies)
    #print cookies
    #session = requests.session(cookies=cookies, headers=HEADERS)
    session = requests.session()
    home = session.get(URL)
    #EVENTVALIDATION = lxml.html.fromstring(home.content).xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value']
    cookies = requests.utils.dict_from_cookiejar(home.cookies)
    while True:
        i += 1
        #FORM_DATA['__EVENTVALIDATION'] = EVENTVALIDATION
        FORM_DATA['__EVENTARGUMENT'] = 'Page$%s' % i
        print FORM_DATA
        response = session.post(URL, data=FORM_DATA, cookies=cookies, headers=POSTHEADERS)
        print i, ' -> ', response.status_code
        print response.content
        html = lxml.html.fromstring(response.content)
        for row in parse_html(html):
            print row
        if i == 20:
            break

main()

