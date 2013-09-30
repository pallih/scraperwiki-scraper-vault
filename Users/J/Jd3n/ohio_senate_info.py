import scraperwiki
import re
import urllib2

SENATE_DIRECTORY = 'http://www.ohiosenate.gov/directory.html'


def find_data(content):
    regex1 = re.compile("class=senator-name style='text-align:left;'>(\w.+) \(.\)</div>",re.IGNORECASE)
    r1 = regex1.search(content)
    find_name = r1.groups()

    regex2 = re.compile("(\w.+?)<br>(\w.+?)<br>(\w.+?)<br>",re.IGNORECASE)
    r2 = regex2.search(content)
    find_address = r2.groups()

    regex3 = re.compile("Phone: (\([0-9].+\)) ([0-9].+)-([0-9].+)<br>")
    r3 = regex3.search(content)
    find_phone = r3.groups()

    regex4 = re.compile('<div class=senator-title>(\w.+)</div>')
    r4 = regex4.search(content)
    find_title = r4.groups()

    regex5 = re.compile("<title>Senator \w.+ \(.\) - District (.*)</title>",re.IGNORECASE)
    r5 = regex5.search(content)
    find_district = r5.groups()

    regex6 = re.compile("Counties:\s(/*.+)</div>",re.IGNORECASE)
    r6 = regex6.search(content)
    find_counties = r6.groups()


    return find_name, find_address, find_phone, find_title, find_district, find_counties


def generate_link_list(url):
    link_list = []

    source = urllib2.urlopen(url).read()

    regex1 = re.compile('<a class=senatorLN href=/(\w.*?)>\w.*?')
    senator_list = regex1.findall(source)

    for senator in senator_list:
        link_list.append("http://www.ohiosenate.gov/%s" % senator)

# For Testing:
#    link_list = ["http://www.ohiosenate.gov/bill-beagle.html", "http://www.ohiosenate.gov/bill-coley.html", "http://www.ohiosenate.gov/eric-kearney.html"]
    
    return link_list


def get_data(link_list):
    data = []
    print link_list
    for link in link_list:
        source = urllib2.urlopen(link).read()
        data.append(find_data(source))

    data_dict = {}

    for item in data:
        name = item[0][0]
        address = "%s, %s, %s" % (item[1][0], item[1][1], item[1][2])
        phone = "%s-%s-%s" % (item[2][0], item[2][1], item[2][2])
        title = item[3][0]
        district = "District %s" % item[4][0]
        county = item[5][0]

        if int(item[4][0]) < 10:
             email = "SD0%s@ohr.state.oh.us" % item[4][0]
        else:
             email = "SD%s@ohr.state.oh.us" % item[4][0]

        if title == "Senator":
            title = ''

        data_dict = {
                        'name': name, 
                        'address': address, 
                        'phone': phone,
                        'title': title,
                        'district': district,
                        'county': county,
                        'email': email,
                    }

        scraperwiki.sqlite.save(unique_keys=['name', 'address', 'phone', 'title', 'district', 'county', 'email'], data=data_dict)

get_data(generate_link_list(SENATE_DIRECTORY))



import scraperwiki
import re
import urllib2

SENATE_DIRECTORY = 'http://www.ohiosenate.gov/directory.html'


def find_data(content):
    regex1 = re.compile("class=senator-name style='text-align:left;'>(\w.+) \(.\)</div>",re.IGNORECASE)
    r1 = regex1.search(content)
    find_name = r1.groups()

    regex2 = re.compile("(\w.+?)<br>(\w.+?)<br>(\w.+?)<br>",re.IGNORECASE)
    r2 = regex2.search(content)
    find_address = r2.groups()

    regex3 = re.compile("Phone: (\([0-9].+\)) ([0-9].+)-([0-9].+)<br>")
    r3 = regex3.search(content)
    find_phone = r3.groups()

    regex4 = re.compile('<div class=senator-title>(\w.+)</div>')
    r4 = regex4.search(content)
    find_title = r4.groups()

    regex5 = re.compile("<title>Senator \w.+ \(.\) - District (.*)</title>",re.IGNORECASE)
    r5 = regex5.search(content)
    find_district = r5.groups()

    regex6 = re.compile("Counties:\s(/*.+)</div>",re.IGNORECASE)
    r6 = regex6.search(content)
    find_counties = r6.groups()


    return find_name, find_address, find_phone, find_title, find_district, find_counties


def generate_link_list(url):
    link_list = []

    source = urllib2.urlopen(url).read()

    regex1 = re.compile('<a class=senatorLN href=/(\w.*?)>\w.*?')
    senator_list = regex1.findall(source)

    for senator in senator_list:
        link_list.append("http://www.ohiosenate.gov/%s" % senator)

# For Testing:
#    link_list = ["http://www.ohiosenate.gov/bill-beagle.html", "http://www.ohiosenate.gov/bill-coley.html", "http://www.ohiosenate.gov/eric-kearney.html"]
    
    return link_list


def get_data(link_list):
    data = []
    print link_list
    for link in link_list:
        source = urllib2.urlopen(link).read()
        data.append(find_data(source))

    data_dict = {}

    for item in data:
        name = item[0][0]
        address = "%s, %s, %s" % (item[1][0], item[1][1], item[1][2])
        phone = "%s-%s-%s" % (item[2][0], item[2][1], item[2][2])
        title = item[3][0]
        district = "District %s" % item[4][0]
        county = item[5][0]

        if int(item[4][0]) < 10:
             email = "SD0%s@ohr.state.oh.us" % item[4][0]
        else:
             email = "SD%s@ohr.state.oh.us" % item[4][0]

        if title == "Senator":
            title = ''

        data_dict = {
                        'name': name, 
                        'address': address, 
                        'phone': phone,
                        'title': title,
                        'district': district,
                        'county': county,
                        'email': email,
                    }

        scraperwiki.sqlite.save(unique_keys=['name', 'address', 'phone', 'title', 'district', 'county', 'email'], data=data_dict)

get_data(generate_link_list(SENATE_DIRECTORY))



