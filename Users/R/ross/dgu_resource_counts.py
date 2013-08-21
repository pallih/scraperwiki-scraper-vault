import csv
import collections
import urllib
import zipfile
import StringIO
import scraperwiki
import sys
import json

source = "http://data.gov.uk/data/dumps/data.gov.uk-ckan-meta-data-latest.csv.zip"
target = "/tmp/latest.csv.zip"

urllib.urlretrieve( source, target )

resources = collections.defaultdict(int)
datasets = collections.defaultdict(int)

csv.field_size_limit(sys.maxsize)

fh = open(target, 'rb')
with zipfile.ZipFile(fh) as zf:
    # Must use namelist because latest is a symlink on the server and the 
    # zipped file has a different name
    data = StringIO.StringIO(zf.read(zf.namelist()[0]))
    reader = csv.DictReader(data)
    for row in reader:
        if not row['groups']:
            # Uhuh.
            continue
        datasets[row['groups']] += 1
        if row['resources']:
            # JSON seems to be a little wobbly so just count a unique string per res_dict
            resources[row['groups']] += row['resources'].count('resource_group')
            #print row['resources'].count('id')

l = []
for k,v in datasets.iteritems():
    row = { "name": k, "datasets": v}
    row["resources"] = resources.get(k, 0)
    l.append(row)
scraperwiki.sqlite.save(["name"], l)

import csv
import collections
import urllib
import zipfile
import StringIO
import scraperwiki
import sys
import json

source = "http://data.gov.uk/data/dumps/data.gov.uk-ckan-meta-data-latest.csv.zip"
target = "/tmp/latest.csv.zip"

urllib.urlretrieve( source, target )

resources = collections.defaultdict(int)
datasets = collections.defaultdict(int)

csv.field_size_limit(sys.maxsize)

fh = open(target, 'rb')
with zipfile.ZipFile(fh) as zf:
    # Must use namelist because latest is a symlink on the server and the 
    # zipped file has a different name
    data = StringIO.StringIO(zf.read(zf.namelist()[0]))
    reader = csv.DictReader(data)
    for row in reader:
        if not row['groups']:
            # Uhuh.
            continue
        datasets[row['groups']] += 1
        if row['resources']:
            # JSON seems to be a little wobbly so just count a unique string per res_dict
            resources[row['groups']] += row['resources'].count('resource_group')
            #print row['resources'].count('id')

l = []
for k,v in datasets.iteritems():
    row = { "name": k, "datasets": v}
    row["resources"] = resources.get(k, 0)
    l.append(row)
scraperwiki.sqlite.save(["name"], l)

