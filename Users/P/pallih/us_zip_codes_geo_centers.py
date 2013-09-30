import scraperwiki
import csv
import re
import os

#found here: http://www.mfasold.net/blog/2010/02/python-recipe-read-csvtsv-textfiles-and-ignore-comment-lines/

class CommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line
    def __iter__(self):
        return self

tsv = scraperwiki.scrape('http://www.census.gov/geo/www/gazetteer/files/Gaz_zcta_national.txt')

tsv_file = csv.reader( tsv.split( os.linesep ),delimiter='\t')

for row in tsv_file:
    record = {}
    record['zip'] = row[0]
    record['land_sqm'] = row[1]
    record['water_sqm'] = row[2]
    record['land_sqmi'] = row[3]
    record['water_sqmi'] = row[4]
    record['lon'] = row[5]
    record['lat'] = row[6]
    scraperwiki.sqlite.save(['zip'], data=record, table_name='us-2010-zipcodes-geo')


import scraperwiki
import csv
import re
import os

#found here: http://www.mfasold.net/blog/2010/02/python-recipe-read-csvtsv-textfiles-and-ignore-comment-lines/

class CommentedFile:
    def __init__(self, f, commentstring="#"):
        self.f = f
        self.commentstring = commentstring
    def next(self):
        line = self.f.next()
        while line.startswith(self.commentstring):
            line = self.f.next()
        return line
    def __iter__(self):
        return self

tsv = scraperwiki.scrape('http://www.census.gov/geo/www/gazetteer/files/Gaz_zcta_national.txt')

tsv_file = csv.reader( tsv.split( os.linesep ),delimiter='\t')

for row in tsv_file:
    record = {}
    record['zip'] = row[0]
    record['land_sqm'] = row[1]
    record['water_sqm'] = row[2]
    record['land_sqmi'] = row[3]
    record['water_sqmi'] = row[4]
    record['lon'] = row[5]
    record['lat'] = row[6]
    scraperwiki.sqlite.save(['zip'], data=record, table_name='us-2010-zipcodes-geo')


