#Pakistan corporations

import scraperwiki
import string
import urllib
import urllib2
import lxml.html
import re
import random
import time

baseurl = 'http://www.secp.gov.pk/ns/index.asp'
posturl= 'http://www.secp.gov.pk/ns/searchresult.asp'
regex_no_matches = re.compile("No matches found.")
regex_number_of_results = re.compile("Total records found : <b>(.*)<\/b>")
regex_id_nr = re.compile("_CODE=(\d+)")

#alphabet = list(string.ascii_lowercase) + list(string.digits) + ['(']

#for letter in alphabet:
#Runtime info setup:
#    record = {}
#    record ['letter'] = letter
#    record ['done'] = '0'
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')
#exit()


selection_statement = '* from runtime_info where done=0'
alphabet = scraperwiki.sqlite.select(selection_statement)


if alphabet:
    random.shuffle(alphabet) # just for fun!

    for l in alphabet:
        values = {'SortBy' : 'a',
          'tName' : l['letter'],
          'rSearch' : 'b' }
        data = urllib.urlencode(values)
        req = urllib2.Request(posturl, data)
        response = urllib2.urlopen(req)
        html = response.read()
        if regex_no_matches.findall(html):
            print "No results for letter: ", l['letter']
            update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"' +l['letter']+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
        else:
            print 'number of results for ', l['letter'], regex_number_of_results.findall(html)[0]
            root = lxml.html.fromstring(html.decode("iso-8859-1"))
            for td in root.xpath('//td[@class="row-1"]/.'):
                record = {}
                name = td.text_content()
                record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
                record['name'] = name
                record['url'] = 'http://www.secp.gov.pk/ns/' + td[0].get('href')
                record['id-nr'] = regex_id_nr.findall(td[0].get('href'))[0]
                scraperwiki.sqlite.save(['name', 'id-nr'], data=record, table_name='pakistan-companies')
            update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"' +l['letter']+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()

else:
    #start again!
    print "All letters have been done - let's do them again!"
    scraperwiki.sqlite.execute("drop table if exists runtime_info")
    alphabet = list(string.ascii_lowercase) + list(string.digits) + ['(']

    for letter in alphabet:
        record = {}
        record ['letter'] = letter
        record ['done'] = '0'
        scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')
    