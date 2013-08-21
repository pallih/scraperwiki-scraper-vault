import scraperwiki
import lxml.html
import re
import urllib
import json



index = 'http://www.ucas.com/students/choosingcourses/choosinguni/instguide/'
letters = ['a']

print 'Checking which letters to scrape...'

html = scraperwiki.scrape(index)

root = lxml.html.fromstring(html)
for a in root.cssselect("#glossary a"):
    letters.append(a.text_content().lower())

for letter in letters:
    print 'Scraping universities starting with the letter ' + letter.upper() + '...'
    temp = []
    html = scraperwiki.scrape(index + letter)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#guide tr"):
        tr.cssselect('a')[-1].drop_tree() # remove the 'further details' text
        h3 = tr.cssselect('h3')[0].text_content()
        td = tr.cssselect('td')[0].text_content().replace(h3,'')
        print 'Extracting raw details for: ' + h3 + '...'
        temp.append({"raw_name":h3, "raw_details":td})
    print "Saving details for " + str(len(temp)) + " universities starting with the letter " + letter.upper() + "..."
    scraperwiki.sqlite.save(unique_keys=["raw_name"], data=temp, table_name="raw_data")

print 'Scrape complete. Now cleaning data...'

raw = scraperwiki.sqlite.select("* from raw_data order by raw_name")

for uni in raw:
    print 'Cleaning ' + uni['raw_name'] + '...'
    temp = {}

    name_search = re.search('^(\w+) - (.+)$', uni['raw_name'])
    if name_search:
        temp['ucas_id'] = name_search.group(1)
        temp['name'] = name_search.group(2)

    address_search = re.search('(.*([A-Z][A-Z]?[0-9][A-Z0-9]? ?[0-9][A-Z][A-Z]))', uni['raw_details'], re.DOTALL)
    if address_search:
        temp['address'] = address_search.group(1).strip()
        postcode_search = re.search('([A-Z][A-Z]?[0-9][A-Z0-9]? ?[0-9][A-Z][A-Z])', temp['address'], re.DOTALL)
        temp['postcode'] = postcode_search.group(1).strip()
        latlng = scraperwiki.geo.gb_postcode_to_latlng(temp['postcode'])
        if latlng:
            temp['latitude'] = latlng[0]
            temp['longitude'] = latlng[1]
        else:
            print 'WARNING: POSTCODE ' + temp['postcode'] + ' RETURNED NO LATITUDE/LONGITUDE'

    phone_search = re.search('t: (.+)', uni['raw_details'])
    if phone_search:
        temp['phone'] = phone_search.group(1).strip()

    email_search = re.search('e: (.+)', uni['raw_details'])
    if email_search:
        temp['email'] = email_search.group(1).strip()

    website_search = re.search('w: (.+)', uni['raw_details'])
    if website_search:
        temp['website'] = website_search.group(1).strip()
        if temp['website'][:4] != 'http':
            temp['website'] = 'http://' + temp['website']

    scraperwiki.sqlite.save(unique_keys=["ucas_id"], data=temp, table_name="universities")



"""
scraperwiki.sqlite.execute("update universities set latitude='53.920658', longitude='-1.161491' where postcode='YO23 3FR'");
scraperwiki.sqlite.execute("update universities set latitude='53.4978295', longitude='-1.3160335' where postcode='S63 7EW'");
scraperwiki.sqlite.execute("update universities set latitude='53.948421', longitude='-1.053545' where postcode='YO10 5DD'");
scraperwiki.sqlite.execute("update universities set latitude='52.591497', longitude='-2.127289' where postcode='WV1 1AD'");
scraperwiki.sqlite.execute("update universities set latitude='53.929647', longitude='-1.112727' where postcode='YO23 2BB'");
scraperwiki.sqlite.execute("update universities set latitude='53.965247', longitude='-1.080281' where postcode='YO31 7EX'");
scraperwiki.sqlite.execute("update universities set latitude='54.284012', longitude='-0.43634' where postcode='YO12 5RN'");
scraperwiki.sqlite.commit()
"""


