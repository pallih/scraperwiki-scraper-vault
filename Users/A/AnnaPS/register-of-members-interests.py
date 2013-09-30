#############################################################################
# Find the number of articles by MPs on journalisted.com
# Uses the TWFY and Journalisted APIs - no actual scraping needed! 
# The Python code just mashes up the two.
# NB: if used for actual research, needs manual checking 
# to ensure MPs aren't confused with similarly-named journalists.
#############################################################################

import scraperwiki
import BeautifulSoup
import json, urllib2

# Order the data columns in a sensible way
scraperwiki.metadata.save('data_columns', ['Name', 'Total articles', 'Party', 'Journalisted URL', 'MP_ID'])

# get all the MPs from the TWFY API & load into a json object
MP_LIST_URL = 'http://www.theyworkforyou.com/api/getMPs?key=APQDY4AnvTLQE5cWLwEdr98x'   
result = json.load(urllib2.urlopen(MP_LIST_URL), encoding='latin-1')

# for each MP, retrieve basic name/party/constituency info
for item in result:
    mp_id = item["person_id"]
    mp_name = item["name"]
    print mp_name
    mp_name_url =  mp_name.replace(' ', '-')
    mp_name_url = urllib2.quote(mp_name_url.lower().encode('latin1'))
    print mp_name_url
    mp_party = item["party"]
    mp_constituency = item["constituency"]
    # replace spaces in name with hyphens 
    journalisted_url = 'http://www.journalisted.com/' + mp_name_url
    # now find the journalisted page for that MP
    JOURNALISTED_API_URL = 'http://journalisted.com/api/getJournoArticles?limit=10000&journo=' + mp_name_url
    journalisted_result = json.load(urllib2.urlopen(JOURNALISTED_API_URL), encoding='latin-1')
    article_count = 0
    for item in journalisted_result["results"]:
         article_count += 1
    if article_count != 0:
        data = {'MP_ID' : mp_id, 'Name' : mp_name,  'Party' : mp_party, 'Total articles' : article_count, 'Journalisted URL' : journalisted_url, }
        print mp_name + " : " + str(article_count) + " articles"
        scraperwiki.datastore.save(unique_keys=['MP_ID'], data=data)

#############################################################################
# Find the number of articles by MPs on journalisted.com
# Uses the TWFY and Journalisted APIs - no actual scraping needed! 
# The Python code just mashes up the two.
# NB: if used for actual research, needs manual checking 
# to ensure MPs aren't confused with similarly-named journalists.
#############################################################################

import scraperwiki
import BeautifulSoup
import json, urllib2

# Order the data columns in a sensible way
scraperwiki.metadata.save('data_columns', ['Name', 'Total articles', 'Party', 'Journalisted URL', 'MP_ID'])

# get all the MPs from the TWFY API & load into a json object
MP_LIST_URL = 'http://www.theyworkforyou.com/api/getMPs?key=APQDY4AnvTLQE5cWLwEdr98x'   
result = json.load(urllib2.urlopen(MP_LIST_URL), encoding='latin-1')

# for each MP, retrieve basic name/party/constituency info
for item in result:
    mp_id = item["person_id"]
    mp_name = item["name"]
    print mp_name
    mp_name_url =  mp_name.replace(' ', '-')
    mp_name_url = urllib2.quote(mp_name_url.lower().encode('latin1'))
    print mp_name_url
    mp_party = item["party"]
    mp_constituency = item["constituency"]
    # replace spaces in name with hyphens 
    journalisted_url = 'http://www.journalisted.com/' + mp_name_url
    # now find the journalisted page for that MP
    JOURNALISTED_API_URL = 'http://journalisted.com/api/getJournoArticles?limit=10000&journo=' + mp_name_url
    journalisted_result = json.load(urllib2.urlopen(JOURNALISTED_API_URL), encoding='latin-1')
    article_count = 0
    for item in journalisted_result["results"]:
         article_count += 1
    if article_count != 0:
        data = {'MP_ID' : mp_id, 'Name' : mp_name,  'Party' : mp_party, 'Total articles' : article_count, 'Journalisted URL' : journalisted_url, }
        print mp_name + " : " + str(article_count) + " articles"
        scraperwiki.datastore.save(unique_keys=['MP_ID'], data=data)

