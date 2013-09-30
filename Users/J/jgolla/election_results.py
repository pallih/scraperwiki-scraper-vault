import scraperwiki
import csv

class Column:
    Ward = 0
    Division = 1
    Type = 2 
    Office = 3
    Name = 4
    Party = 5
    Votes = 6

base_url = 'http://www.campaignscientific.com/Downloads/PhilaElecResults/'

years = [ '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010' ]
result_types = [ 'GENERAL', 'PRIMARY', 'SPECIAL' ]

#years = [ '2002' ]
#result_types = [ 'SPECIAL' ]

index = 0

for year in years:
    print "process year : " + year
    for result_type in result_types:
        print "processing type : " + result_type
        try:
            data = scraperwiki.scrape(base_url + year + "_" + result_type + ".txt")
            reader = csv.reader(data.splitlines(), 'excel-tab')
            for row in reader:
                if (row[Column.Ward] != 'WARD' and row[Column.Office] != "No Vote"):
                    record = { 'index' : index, 'year': year, 'election_type' : result_type, 'ward' : row[Column.Ward], 'division' : row[Column.Division], 'type' : row[Column.Type], 'office' : row[Column.Office], 'name': row[Column.Name], 'party' : row[Column.Party], 'votes' : row[Column.Votes]}
                    scraperwiki.sqlite.save(['index'], record)
                    index = index + 1
        except:
            print "Error occured"

import scraperwiki
import csv

class Column:
    Ward = 0
    Division = 1
    Type = 2 
    Office = 3
    Name = 4
    Party = 5
    Votes = 6

base_url = 'http://www.campaignscientific.com/Downloads/PhilaElecResults/'

years = [ '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010' ]
result_types = [ 'GENERAL', 'PRIMARY', 'SPECIAL' ]

#years = [ '2002' ]
#result_types = [ 'SPECIAL' ]

index = 0

for year in years:
    print "process year : " + year
    for result_type in result_types:
        print "processing type : " + result_type
        try:
            data = scraperwiki.scrape(base_url + year + "_" + result_type + ".txt")
            reader = csv.reader(data.splitlines(), 'excel-tab')
            for row in reader:
                if (row[Column.Ward] != 'WARD' and row[Column.Office] != "No Vote"):
                    record = { 'index' : index, 'year': year, 'election_type' : result_type, 'ward' : row[Column.Ward], 'division' : row[Column.Division], 'type' : row[Column.Type], 'office' : row[Column.Office], 'name': row[Column.Name], 'party' : row[Column.Party], 'votes' : row[Column.Votes]}
                    scraperwiki.sqlite.save(['index'], record)
                    index = index + 1
        except:
            print "Error occured"

