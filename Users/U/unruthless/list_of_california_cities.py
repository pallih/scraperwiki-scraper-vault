# #############################################################################
# LIBRARIES

import scraperwiki
import urllib
import lxml.html as lh
import mechanize
import re
import simplejson

from time import sleep

# #############################################################################
# MECHANIZE

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# #############################################################################
# SEARCH ENGINES

def google(q):
    query = urllib.urlencode({'q' : q})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    if json['responseData']:
        results = json['responseData']['results']
        return results[0]['url']
    else:
        print json

def bing(q):
    query = urllib.urlencode({'Query' : removeNonAscii(q)})
    url = 'http://api.bing.net/json.aspx?AppId=C83ABEA1F7FF250C9CB4E9F674DECC9666406954&Version=2.2&Market=en-US&JsonType=raw&Sources=web&%s' % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    if json['SearchResponse']['Web']['Results']:
        results = json['SearchResponse']['Web']['Results']
        print q
        return results[0]['Url']
    else:
        print json

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


# #############################################################################
# DATA SOURCES
#  
# Municipalities:
# http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California
#
# Municipal Codes:
# http://california.lp.findlaw.com/ca01_codes/municode.html
# http://www.municode.com/Library/CA

html_municipalities = br.open("http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California")

# #############################################################################
# PARSE HTML

municipalities = lh.fromstring(html_municipalities.read()).cssselect('table.plainrowheaders tr')

data = []

print "Processing..."

for row in municipalities[1:]:

    municipality = {
        "municipality_name":               row[0].text_content(),
        "municipality_type":               row[1].text_content(),
        "municipality_county":             row[2].text_content(),
        "municipality_population_2010":    int(re.sub(r'\[\d+\]', '', row[3].text_content().replace(",",""))),
        "municipality_incorporation_date": int(row[5].text_content()[1:5]),
        "municipal_code_url":              bing(row[0].text_content() + ", CA Municipal Code")
    }
    data.append(municipality)
    sleep(1)


# #############################################################################
# WRITE TO DATABASE

# scraperwiki.sqlite.execute("""
# DROP TABLE IF EXISTS ca_municipalities_and_bike_licensing
# """)

# scraperwiki.sqlite.execute("""
# CREATE TABLE `ca_municipalities_and_bike_licensing`
# (
#    `municipality_name`               text,
#    `municipality_type`               text,
#    `municipality_county`             text,
#    `municipality_population_2010`    int,
#    `municipality_incorporation_date` int,
#    `municipal_code_url`              text
# )
# """)

scraperwiki.sqlite.save(["municipality_name"],data,"ca_municipalities_and_bike_licensing")
# #############################################################################
# LIBRARIES

import scraperwiki
import urllib
import lxml.html as lh
import mechanize
import re
import simplejson

from time import sleep

# #############################################################################
# MECHANIZE

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# #############################################################################
# SEARCH ENGINES

def google(q):
    query = urllib.urlencode({'q' : q})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    if json['responseData']:
        results = json['responseData']['results']
        return results[0]['url']
    else:
        print json

def bing(q):
    query = urllib.urlencode({'Query' : removeNonAscii(q)})
    url = 'http://api.bing.net/json.aspx?AppId=C83ABEA1F7FF250C9CB4E9F674DECC9666406954&Version=2.2&Market=en-US&JsonType=raw&Sources=web&%s' % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    if json['SearchResponse']['Web']['Results']:
        results = json['SearchResponse']['Web']['Results']
        print q
        return results[0]['Url']
    else:
        print json

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


# #############################################################################
# DATA SOURCES
#  
# Municipalities:
# http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California
#
# Municipal Codes:
# http://california.lp.findlaw.com/ca01_codes/municode.html
# http://www.municode.com/Library/CA

html_municipalities = br.open("http://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California")

# #############################################################################
# PARSE HTML

municipalities = lh.fromstring(html_municipalities.read()).cssselect('table.plainrowheaders tr')

data = []

print "Processing..."

for row in municipalities[1:]:

    municipality = {
        "municipality_name":               row[0].text_content(),
        "municipality_type":               row[1].text_content(),
        "municipality_county":             row[2].text_content(),
        "municipality_population_2010":    int(re.sub(r'\[\d+\]', '', row[3].text_content().replace(",",""))),
        "municipality_incorporation_date": int(row[5].text_content()[1:5]),
        "municipal_code_url":              bing(row[0].text_content() + ", CA Municipal Code")
    }
    data.append(municipality)
    sleep(1)


# #############################################################################
# WRITE TO DATABASE

# scraperwiki.sqlite.execute("""
# DROP TABLE IF EXISTS ca_municipalities_and_bike_licensing
# """)

# scraperwiki.sqlite.execute("""
# CREATE TABLE `ca_municipalities_and_bike_licensing`
# (
#    `municipality_name`               text,
#    `municipality_type`               text,
#    `municipality_county`             text,
#    `municipality_population_2010`    int,
#    `municipality_incorporation_date` int,
#    `municipal_code_url`              text
# )
# """)

scraperwiki.sqlite.save(["municipality_name"],data,"ca_municipalities_and_bike_licensing")
