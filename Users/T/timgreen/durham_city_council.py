###############################################################################
# Durham City council scraper
###############################################################################

import scraperwiki
import lxml.html
import re

def do_councillors():
    tree = lxml.html.parse('http://www.durham.gov.uk/pages/Councillors.aspx?OrderBy=Surname&Page=1')
    
    pages = set([1])
    for a in tree.xpath('//a'):
        if 'href' in a.attrib and 'pages/Councillors.aspx?OrderBy=Surname&Page=' in a.attrib['href']:
            pages.add(int(a.attrib['href'][len('/pages/Councillors.aspx?OrderBy=Surname&Page='):]))
    
    print pages
    
    councillors = []
    for page_num in pages:
        tree = lxml.html.parse('http://www.durham.gov.uk/pages/Councillors.aspx?OrderBy=Surname&Page=%d' % page_num)
    
        table = tree.xpath('//table[@class="styledtable"]')[0]
        for row in table:
           items = row.xpath('td')
           if len(items) != 0:
               name = items[0].xpath('a')[0].text
               surname, firstname = name.split(',')
               name = "%s %s" % (firstname, surname)
               url = items[0].xpath('a/@href')[0]
               ward = items[1].text
               party = items[2].text
               councillors.append({'name': name, 'url': url, 'ward': ward, 'party': party})
    
    scraperwiki.sqlite.save(['url'], councillors, table_name='councillors')

def do_committees():
    tree = lxml.html.parse('http://www.durham.gov.uk/pages/displayminutes.aspx')
    
    committees = []
    minutes_url_stub = 'http://www.durham.gov.uk/Pages/displayminutes.aspx?comid='
    
    for a in tree.xpath('//li[@class="AspNet-TreeView-Root AspNet-TreeView-Leaf"]/a'):
        if 'href' in a.attrib and minutes_url_stub in a.attrib['href']:
            url = a.attrib['href']
            id = int(a.attrib['href'][len(minutes_url_stub):])
            name = a.text.strip()

            committees.append({'url': url, 'id': id, 'name': name,})
            

    scraperwiki.sqlite.save(['id'], committees, table_name='committees')

def do_committee_membership():
    committees = scraperwiki.sqlite.select('* from committees;')

    committee_membership = []
    for committee in committees:
        tree = lxml.html.parse(committee['url'])
        for member in tree.xpath('//li[@class="AspNet-TreeView-Leaf"]/a'):
            if 'href' in member.attrib and '/Pages/CouncillorDetails.aspx?Councillor=' in member.attrib['href']:
                member_url = member.attrib['href']
                member_name = member.text

                committee_membership.append({'member_url': member_url, 'committee_id': committee['id'],})

    scraperwiki.sqlite.save(['member_url', 'committee_id'], committee_membership, table_name='committee_membership')

def do_councillors_extra():
    councillors = scraperwiki.sqlite.select('* from councillors')

    address_re = re.compile(r'<h3>Address</h3>(.*?)<br /><br />')
    telephone_re = re.compile(r'<h3>Telephone</h3>(.*?)<br /><br />')
    email_re = re.compile(r'<h3>Email</h3><a href="mailto:(.*?)">.*?</a>')
    for councillor in councillors:
        print councillor['name']
        html = scraperwiki.scrape("http://www.durham.gov.uk%s" % councillor['url'])
        addresses = address_re.findall(html)
        telephones = telephone_re.findall(html)
        emails = email_re.findall(html)

        try:
            councillor['address'] = addresses[0].replace('<br />', '\n')
        except KeyError:
            councillor['address'] = None

        try:
            councillor['telephone'] = telephones[0]
        except KeyError:
            councillor['telephone'] = None

        try:
            councillor['email'] = emails[0]
        except:
            councillor['email'] = None

        scraperwiki.sqlite.save(['url'], councillor, table_name='councillors')
        

do_councillors()
do_committees()
do_committee_membership()
do_councillors_extra()

###############################################################################
# Durham City council scraper
###############################################################################

import scraperwiki
import lxml.html
import re

def do_councillors():
    tree = lxml.html.parse('http://www.durham.gov.uk/pages/Councillors.aspx?OrderBy=Surname&Page=1')
    
    pages = set([1])
    for a in tree.xpath('//a'):
        if 'href' in a.attrib and 'pages/Councillors.aspx?OrderBy=Surname&Page=' in a.attrib['href']:
            pages.add(int(a.attrib['href'][len('/pages/Councillors.aspx?OrderBy=Surname&Page='):]))
    
    print pages
    
    councillors = []
    for page_num in pages:
        tree = lxml.html.parse('http://www.durham.gov.uk/pages/Councillors.aspx?OrderBy=Surname&Page=%d' % page_num)
    
        table = tree.xpath('//table[@class="styledtable"]')[0]
        for row in table:
           items = row.xpath('td')
           if len(items) != 0:
               name = items[0].xpath('a')[0].text
               surname, firstname = name.split(',')
               name = "%s %s" % (firstname, surname)
               url = items[0].xpath('a/@href')[0]
               ward = items[1].text
               party = items[2].text
               councillors.append({'name': name, 'url': url, 'ward': ward, 'party': party})
    
    scraperwiki.sqlite.save(['url'], councillors, table_name='councillors')

def do_committees():
    tree = lxml.html.parse('http://www.durham.gov.uk/pages/displayminutes.aspx')
    
    committees = []
    minutes_url_stub = 'http://www.durham.gov.uk/Pages/displayminutes.aspx?comid='
    
    for a in tree.xpath('//li[@class="AspNet-TreeView-Root AspNet-TreeView-Leaf"]/a'):
        if 'href' in a.attrib and minutes_url_stub in a.attrib['href']:
            url = a.attrib['href']
            id = int(a.attrib['href'][len(minutes_url_stub):])
            name = a.text.strip()

            committees.append({'url': url, 'id': id, 'name': name,})
            

    scraperwiki.sqlite.save(['id'], committees, table_name='committees')

def do_committee_membership():
    committees = scraperwiki.sqlite.select('* from committees;')

    committee_membership = []
    for committee in committees:
        tree = lxml.html.parse(committee['url'])
        for member in tree.xpath('//li[@class="AspNet-TreeView-Leaf"]/a'):
            if 'href' in member.attrib and '/Pages/CouncillorDetails.aspx?Councillor=' in member.attrib['href']:
                member_url = member.attrib['href']
                member_name = member.text

                committee_membership.append({'member_url': member_url, 'committee_id': committee['id'],})

    scraperwiki.sqlite.save(['member_url', 'committee_id'], committee_membership, table_name='committee_membership')

def do_councillors_extra():
    councillors = scraperwiki.sqlite.select('* from councillors')

    address_re = re.compile(r'<h3>Address</h3>(.*?)<br /><br />')
    telephone_re = re.compile(r'<h3>Telephone</h3>(.*?)<br /><br />')
    email_re = re.compile(r'<h3>Email</h3><a href="mailto:(.*?)">.*?</a>')
    for councillor in councillors:
        print councillor['name']
        html = scraperwiki.scrape("http://www.durham.gov.uk%s" % councillor['url'])
        addresses = address_re.findall(html)
        telephones = telephone_re.findall(html)
        emails = email_re.findall(html)

        try:
            councillor['address'] = addresses[0].replace('<br />', '\n')
        except KeyError:
            councillor['address'] = None

        try:
            councillor['telephone'] = telephones[0]
        except KeyError:
            councillor['telephone'] = None

        try:
            councillor['email'] = emails[0]
        except:
            councillor['email'] = None

        scraperwiki.sqlite.save(['url'], councillor, table_name='councillors')
        

do_councillors()
do_committees()
do_committee_membership()
do_councillors_extra()

