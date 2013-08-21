import scraperwiki
import scrapemark
import urllib
import sys
import time
import re

def get_list(page=0):
    read = True
    while read:
        num_items = 100
        url = 'https://epetitionen.bundestag.de/index.php?action=petition;sa=list4;limit=100;start=%d;sort=pet_id;dir=down' % (page * num_items)
        html = urllib.urlopen(url).read()
        #print html
        data = scrapemark.scrape("""
        {*
            <tr>
                <td>{{ [petitions].id|int }}</td>
                <td><a>{{ [petitions].title }}</a></td>
                <td>{{ [petitions].creator }}</td>
                <td>{{ [petitions].enddate }}</td>
                <td>{{ [petitions].signers }}</td>
                <td>{{ [petitions].forumposts }}</td>
            </tr>
        *}
        """, html=html)
        rows = []
        for dataset in data['petitions']:
            # end date
            enddate_match = re.match(r'([0-9]+)\.([0-9]+)\.([0-9]+).*', dataset['enddate'])
            if enddate_match is not None:
                dataset['enddate'] = '-'.join([enddate_match.group(3), enddate_match.group(2), enddate_match.group(1)])
            # signers
            signers_match = re.match(r'([0-9]+).*', dataset['signers'])
            if signers_match is not None:
                dataset['signers'] = int(signers_match.group(1))
            # forum posts
            forumposts_match = re.match(r'([0-9]+).*', dataset['forumposts'])
            if forumposts_match is not None:
                dataset['forumposts'] = int(forumposts_match.group(1))
            #print dataset
            rows.append(dataset)
        # save data
        scraperwiki.sqlite.save(['id'], rows, table_name="petitions")
        if len(data['petitions']) < num_items:
            read = False
            #print "On page " + str(page) + " the number of items is less than "+ str(num_items) +": " + str(len(data['petitions']))
        page += 1
        time.sleep(1)

get_list()