import scraperwiki
import re
import urllib2

COUNTY_DICT = {'1': ['Wayne'], '2': ['Richland'], '3': ['Wood'], '4': ['Allen'], '5': ['Columbiana'], '6': ['Cuyahoga'], '7': ['Cuyahoga'], '8': ['Cuyahoga'], '9': ['Cuyahoga'], '10': ['Cuyahoga'], '11': ['Cuyahoga'], '12': ['Cuyahoga'], '13': ['Cuyahoga'], '14': ['Cuyahoga'], '15': ['Cuyahoga'], '16': ['Cuyahoga'], '17': ['Franklin'], '18': ['Franklin'], '19': ['Franklin'], '20': ['Franklin'], '21': ['Franklin'], '22': ['Franklin'], '23': ['Franklin'], '24': ['Franklin'], '25': ['Franklin'], '26': ['Franklin'], '27': ['Hamilton'], '28': ['Hamilton'], '29': ['Hamilton'], '30': ['Hamilton'], '31': ['Hamilton'], '32': ['Hamilton'], '33': ['Hamilton'], '34': ['Summit'], '35': ['Summit'], '36': ['Summit'], '37': ['Summit'], '38': ['Stark', 'Summit'], '39': ['Montgomery'], '40': ['Montgomery'], '41': ['Montgomery'], '42': ['Montgomery'], '43': ['Montgomery', 'Preble'], '44': ['Lucas'], '45': ['Lucas'], '46': ['Lucas'], '47': ['Fulton', 'Lucas'], '48': ['Stark'], '49': ['Stark'], '50': ['Stark'], '51': ['Butler'], '52': ['Butler'], '53': ['Butler'], '54': ['Butler', 'Warren'], '55': ['Lorain'], '56': ['Lorain'], '57': ['Huron', 'Lorain'], '58': ['Mahoning'], '59': ['Mahoning'], '60': ['Lake'], '61': ['Lake'], '62': ['Warren'], '63': ['Trumbull'], '64': ['Ashtabula', 'Trumbull'], '65': ['Clermont'], '66': ['Brown', 'Clermont'], '67': ['Delaware'], '68': ['Delaware', 'Knox'], '69': ['Medina'], '70': ['Ashland', 'Holmes', 'Medina'], '71': ['Licking'], '72': ['Coshocton', 'Licking', 'Perry'], '73': ['Greene'], '74': ['Clark', 'Greene', 'Madison'], '75': ['Portage'], '76': ['Geauga', 'Portage'], '77': ['Fairfield'], '78': ['Athens', 'Fairfield', 'Hocking', 'Morgan', 'Muskingum', 'Pickaway'], '79': ['Clark'], '80': ['Darke', 'Miami'], '81': ['Fulton', 'Henry', 'Putnam', 'Williams'], '82': ['Auglaize', 'Defiance', 'Paulding', 'Van Wert'], '83': ['Hancock', 'Hardin', 'Logan'], '84': ['Auglaize', 'Darke', 'Mercer', 'Shelby'], '85': ['Champaign', 'Logan', 'Shelby'], '86': ['Marion', 'Union'], '87': ['Crawford', 'Marion', 'Morrow', 'Seneca', 'Wyandot'], '88': ['Sandusky', 'Seneca'], '89': ['Erie', 'Ottawa'], '90': ['Adams', 'Lawrence', 'Scioto'], '91': ['Clinton', 'Highland', 'Pike', 'Ross'], '92': ['Fayette', 'Pickaway', 'Ross'], '93': ['Gallia', 'Jackson', 'Lawrence', 'Vinton'], '94': ['Athens', 'Meigs', 'Vinton', 'Washington'], '95': ['Belmont', 'Carroll', 'Harrison', 'Noble', 'Washington'], '96': ['Belmont', 'Jefferson', 'Monroe'], '97': ['Guernsey', 'Muskingum'], '98': ['Holmes', 'Tuscarawas'], '99': ['Ashtabula', 'Geauga']}

def find_names():
    regex_names = re.compile("<div class='data'><h3><a class='black' href='..\/\w.+?'>(\w.+?)</a>")
    return regex_names.findall(urllib2.urlopen("http://www.ohiohouse.gov/members/member-directory").read())

def create_urls(names):
    url_list = []
    for name in names:
        name_list = name.lower().split()
        final_name_list = []
        for item in name_list:
            item = re.sub("[^A-Za-z]", "", item)
            final_name_list.append(item)
        name = '-'.join(final_name_list)
        url_list.append("http://www.ohiohouse.gov/%s" % name)
    return url_list

def find_data(url_list):
    for url in url_list:
        source = urllib2.urlopen(url).read()
        # Gets name, district number, address, phone, and fax
        regex1 = re.compile("div class='contactHeader'>\s+Representative (\w.+?)<br />\s+District (\d+)\s+</div>\s+(\w.+) <br />\s+(\w.+) <br />\s+(\w.+) <br />\s+(Phone)&nbsp(\([0-9].+\) [0-9].+-[0-9].+) <br />\s+(Fax)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp(\([0-9].+\) [0-9].+-[0-9].+) <br />")
        r1 = regex1.search(source)
        contact_info = r1.groups()

        # Gets Hometown
        regex_hometown = re.compile("<strong>Hometown</strong>\s+:\s+(\w.+?)\s+<br />")
        rHome = regex_hometown.search(source)
        if rHome:
            hometown = rHome.groups()[0]
        else:
            hometown = ''

        # Gets Party
        regex_party = re.compile("<strong>Party</strong>\s+:\s+(\w.+?)\s+<br />")
        rParty = regex_party.search(source)
        party = rParty.groups()[0]

        # Gets Term
        regex_term = re.compile ("<strong>Current\s+Term</strong>\s+:\s+(\w.+?)\s+</div>")
        rTerm = regex_term.search(source)
        term = rTerm.groups()[0]

        # Gets Leadership Position
        regex_lead = re.compile ("<strong>Leadership\s+Position</strong>\s+:\s+(\w.+?)<br />")
        rLead = regex_lead.search(source)
        if rLead:
            lead = rLead.groups()[0]
        else:
            lead = ''

        # separtes resulting lists into variables
        name = contact_info[0]
        district = contact_info[1]
        address = "%s, %s, %s" % (contact_info[2], contact_info[3], contact_info[4])
        phone = contact_info[6]
        fax = contact_info[8]
        county = ', '.join(COUNTY_DICT[district])
        email = "district%s@ohr.state.oh.us" % district

        # adds info to scraperwiki datastore
        data_dict = {
                        'name': name, 
                        'address': address, 
                        'phone': phone,
                        'fax': fax,
                        'district': district,
                        'email': email,
                        'county': county,
                        'hometown': hometown,
                        'party': party,
                        'term': term,
                        'leadership': lead,
                    }

        scraperwiki.sqlite.save(unique_keys=['name', 
                                             'address', 
                                             'phone', 
                                             'fax', 
                                             'district', 
                                             'email', 
                                             'county',
                                             'hometown',
                                             'party',
                                             'term',
                                             'leadership'], data=data_dict)

find_data(create_urls(find_names()))
