#api b28b6999c1e40dd9e1133edee8f83305


import scraperwiki
import csv
from scraperwiki import datastore

for year, quarter, partnum, url in [(2002, 1, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q1/qmcw_download.csv'),
                                    (2002, 2, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q2/qmcw_download.csv'),
                                    (2002, 3, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q3/qmcw_download.csv'),
                                    (2002, 4, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q4/qmcw_download.csv'),
                                    (2003, 1, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q1/qmcw_download.csv'),
                                    (2003, 2, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q2/qmcw_download.csv'),
                                    (2003, 3, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q3/qmcw_download.csv'),
                                    (2003, 4, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q4/qmcw_download.csv'),
                                    ]:
    csvdata = scraperwiki.scrape(url)
    parts = csvdata.split("\nPart")
    ids = 0
    for part in parts:
        print part
        heading = part.splitlines()[0].split(":")
        print year, quarter, heading
        print heading[0].strip(), partnum,  heading[0].strip() == partnum
        if heading[0].strip() == partnum:
            print "Parsing"
            dr = csv.DictReader(part.splitlines()[1:])
            r = True
            for data in dr:
                data['Id'] = ids
                ids += 1
                data["Year"] = year
                data["Quarter"] = quarter
                datastore.save(unique_keys=['Id'], data=data)


#api b28b6999c1e40dd9e1133edee8f83305


import scraperwiki
import csv
from scraperwiki import datastore

for year, quarter, partnum, url in [(2002, 1, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q1/qmcw_download.csv'),
                                    (2002, 2, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q2/qmcw_download.csv'),
                                    (2002, 3, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q3/qmcw_download.csv'),
                                    (2002, 4, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2002/q4/qmcw_download.csv'),
                                    (2003, 1, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q1/qmcw_download.csv'),
                                    (2003, 2, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q2/qmcw_download.csv'),
                                    (2003, 3, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q3/qmcw_download.csv'),
                                    (2003, 4, "4", 'http://www.performance.doh.gov.uk/cancerwaits/2003/q4/qmcw_download.csv'),
                                    ]:
    csvdata = scraperwiki.scrape(url)
    parts = csvdata.split("\nPart")
    ids = 0
    for part in parts:
        print part
        heading = part.splitlines()[0].split(":")
        print year, quarter, heading
        print heading[0].strip(), partnum,  heading[0].strip() == partnum
        if heading[0].strip() == partnum:
            print "Parsing"
            dr = csv.DictReader(part.splitlines()[1:])
            r = True
            for data in dr:
                data['Id'] = ids
                ids += 1
                data["Year"] = year
                data["Quarter"] = quarter
                datastore.save(unique_keys=['Id'], data=data)


