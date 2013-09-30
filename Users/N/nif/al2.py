from string import ascii_lowercase
import urllib2
import re
import scraperwiki
import lxml.html           
import urlparse


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
    }
    request = urllib2.Request(url, headers=headers)
    try:
        return urllib2.urlopen(request).read()
    except IOError, e:
        if hasattr(e, 'reason'):
            print "We failed to reach a server."
            print "Reason: ", e.reason
        elif hasattr(e, 'code'):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        return None

def parse_birth_data(data):
    birth_date = ""
    birth_place = ""
    if "-" in data:
        birth_date, birth_place = data.split(" - ", 1)
    else:
        if re.match(r"\d{2}/\d{2}/\d{4}", data):
            birth_date = data
        else:
            birth_place = data
    return birth_date, birth_place

def parse_birth_data2(data):
    birth_data_re = re.compile(r"(?P<date>(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4}))?(?: - )?(?P<place>.*)")
    data_match = birth_data_re.match(data)
    return data_match.groupdict("")


# scrape_athletes_list function: gets passed an individual page to scrape
def scrape_athletes_list(root):
    rows = root.cssselect("ul.athletesList li")  # selects all <li> blocks within <ul class="athletesList">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Url'] = row.cssselect("div.athleteName a")[0].attrib.get('href')
        record['Name'] = row.cssselect("span.athletePassportName")[0].text
        record['Surname'] = row.cssselect("span.athletePassportSurname")[0].text
        record['Country'] = row.cssselect("div.country img")[0].attrib.get('alt')
        record['CountryCode'] = row.cssselect("span.noc")[0].text
        record['Sport'] = row.cssselect("div.disc a")[0].text
        # Get more personal data
        try:
            personal_url = urlparse.urljoin(base_url, record['Url'])
            print personal_url
            personal_html = get_html(personal_url)
            if personal_html:
                personal_root = lxml.html.fromstring(personal_html)
                bio = personal_root.cssselect("table.athleteBio tr")
                birth_data = bio[3].cssselect("td")[0].text_content()
                birth_data_dict = parse_birth_data2(birth_data)
                record['Birthdate'] = birth_data_dict['date']
                record['Birthday'] = birth_data_dict['day']
                record['Birthmonth'] = birth_data_dict['month']
                record['Birthyear'] = birth_data_dict['year']
                record['Birthplace'] = birth_data_dict['place']
                
                record['Age'] = bio[3].cssselect("td")[1].text_content()
                #other_data = bio[7].cssselect("td")[0].text_content()
                # print other_data
                record['Gender'] = bio[7].cssselect("td:last-child")[0].text_content()
        except (lxml.etree.XMLSyntaxError, urllib2.HTTPError):
            print "Error getting personal page."

        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(unique_keys=["Url"], data=record)

def scrape_and_look_for_next_link(url, page_num = 1):
    page_url = url + ",page=%s.htmx" % page_num
    print page_url
    html = get_html(page_url)
    if html:
        root = lxml.html.fromstring(html)
        scrape_athletes_list(root)
        nores = root.cssselect("div.nores")
        if not nores:
            page_num += 1
            scrape_and_look_for_next_link(url, page_num)

base_url = "http://www.london2012.com"
for begin in ascii_lowercase:
    starting_url = urlparse.urljoin(base_url, '/athletes/initial=%s/index' % begin)
    print starting_url
    scrape_and_look_for_next_link(starting_url)
from string import ascii_lowercase
import urllib2
import re
import scraperwiki
import lxml.html           
import urlparse


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
    }
    request = urllib2.Request(url, headers=headers)
    try:
        return urllib2.urlopen(request).read()
    except IOError, e:
        if hasattr(e, 'reason'):
            print "We failed to reach a server."
            print "Reason: ", e.reason
        elif hasattr(e, 'code'):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        return None

def parse_birth_data(data):
    birth_date = ""
    birth_place = ""
    if "-" in data:
        birth_date, birth_place = data.split(" - ", 1)
    else:
        if re.match(r"\d{2}/\d{2}/\d{4}", data):
            birth_date = data
        else:
            birth_place = data
    return birth_date, birth_place

def parse_birth_data2(data):
    birth_data_re = re.compile(r"(?P<date>(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4}))?(?: - )?(?P<place>.*)")
    data_match = birth_data_re.match(data)
    return data_match.groupdict("")


# scrape_athletes_list function: gets passed an individual page to scrape
def scrape_athletes_list(root):
    rows = root.cssselect("ul.athletesList li")  # selects all <li> blocks within <ul class="athletesList">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Url'] = row.cssselect("div.athleteName a")[0].attrib.get('href')
        record['Name'] = row.cssselect("span.athletePassportName")[0].text
        record['Surname'] = row.cssselect("span.athletePassportSurname")[0].text
        record['Country'] = row.cssselect("div.country img")[0].attrib.get('alt')
        record['CountryCode'] = row.cssselect("span.noc")[0].text
        record['Sport'] = row.cssselect("div.disc a")[0].text
        # Get more personal data
        try:
            personal_url = urlparse.urljoin(base_url, record['Url'])
            print personal_url
            personal_html = get_html(personal_url)
            if personal_html:
                personal_root = lxml.html.fromstring(personal_html)
                bio = personal_root.cssselect("table.athleteBio tr")
                birth_data = bio[3].cssselect("td")[0].text_content()
                birth_data_dict = parse_birth_data2(birth_data)
                record['Birthdate'] = birth_data_dict['date']
                record['Birthday'] = birth_data_dict['day']
                record['Birthmonth'] = birth_data_dict['month']
                record['Birthyear'] = birth_data_dict['year']
                record['Birthplace'] = birth_data_dict['place']
                
                record['Age'] = bio[3].cssselect("td")[1].text_content()
                #other_data = bio[7].cssselect("td")[0].text_content()
                # print other_data
                record['Gender'] = bio[7].cssselect("td:last-child")[0].text_content()
        except (lxml.etree.XMLSyntaxError, urllib2.HTTPError):
            print "Error getting personal page."

        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(unique_keys=["Url"], data=record)

def scrape_and_look_for_next_link(url, page_num = 1):
    page_url = url + ",page=%s.htmx" % page_num
    print page_url
    html = get_html(page_url)
    if html:
        root = lxml.html.fromstring(html)
        scrape_athletes_list(root)
        nores = root.cssselect("div.nores")
        if not nores:
            page_num += 1
            scrape_and_look_for_next_link(url, page_num)

base_url = "http://www.london2012.com"
for begin in ascii_lowercase:
    starting_url = urlparse.urljoin(base_url, '/athletes/initial=%s/index' % begin)
    print starting_url
    scrape_and_look_for_next_link(starting_url)
