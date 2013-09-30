import scraperwiki
import requests
import csv
import lxml.html

'''
# THE STREET NAME COLLECTION
url = 'http://www.postur.is/gogn/Gotuskra/gotuskra.txt'

response = requests.get(url).text
response = response.encode('iso-8859-1')
print response


reader = csv.reader(response.splitlines(),delimiter=';')
headerline = reader.next()
#reader = csv.DictReader(response.splitlines(),delimiter=';')

data = []

for row in reader:
    x = {}
    x['key'] = row[0].decode('iso-8859-1')
    x['zip'] = row[1].decode('iso-8859-1')
    x['nefnifall'] = row[2].decode('iso-8859-1')
    x['thagufall'] = row[3].decode('iso-8859-1')
    data.append(x)
    
print data

exit()
scraperwiki.sqlite.save(unique_keys=['key'], data=data)
'''



# THE NAME COLLECTION



scraperwiki.sqlite.execute("drop table if exists boys")
scraperwiki.sqlite.execute("drop table if exists girls")

#Boys

url = 'http://www.island.is/islensk-nofn?Stafrof=&Nafn=&Drengir=on&Samthykkt=yes'
response = requests.get(url).text
root = root = lxml.html.fromstring(response)
names = root.xpath('//ul[@class="dir"]/li')
data = []
counter = 1
for x in names:
    if x.text != None:
        record = {}
        record['name'] = x.text.strip()
        record['key'] = counter
        data.append(record)
        counter = counter+1
print data
scraperwiki.sqlite.save(unique_keys=['key'], data=data,table_name='boys')

#Girls

url = 'http://www.island.is/islensk-nofn?Stafrof=&Nafn=&Stulkur=on&Samthykkt=yes'
response = requests.get(url).text
root = root = lxml.html.fromstring(response)
names = root.xpath('//ul[@class="dir"]/li')
data = []
counter = 1
for x in names:
    if x.text != None:
        record = {}
        record['name'] = x.text.strip()
        record['key'] = counter
        data.append(record)
        counter = counter+1
scraperwiki.sqlite.save(unique_keys=['key'], data=data,table_name='girls')


# MATCHING
'''
scraperwiki.sqlite.execute("drop table if exists matching_boys")
scraperwiki.sqlite.execute("drop table if exists matching_girls")

#select only the zipz in reykjavik
streets = scraperwiki.sqlite.select('* from "swdata" where "zip" like "10%" OR "zip" like "116"')

#select the boys and the girls
boys = scraperwiki.sqlite.select("name from boys")
girls = scraperwiki.sqlite.select("name from girls")
boys_names = []
girls_names = []
streets_nefnifall = []

#put streets, boys and girl names into lists
for street in streets:
    streets_nefnifall.append(street['nefnifall'])
for name in boys:
    boys_names.append(name['name'])
for name in girls:
    girls_names.append(name['name'])

#match the boys names agains the streets
matching_boys = []
for name in boys_names:
    match = filter(lambda x: name in x,streets_nefnifall)
    if match != []:
        for x in match:
            record = {}
            record['name'] = name
            record['matching_street'] = x
            matching_boys.append(record)


#match the girls names agains the streets
matching_girls = []
for name in girls_names:
    match = filter(lambda x: name in x,streets_nefnifall)
    if match != []:
        for x in match:
            record = {}
            record['name'] = name
            record['matching_street'] = x
            matching_girls.append(record)

#save the matches into two tables

scraperwiki.sqlite.save(unique_keys=['matching_street'], data=matching_boys,table_name='matching_boys')
scraperwiki.sqlite.save(unique_keys=['matching_street'], data=matching_girls,table_name='matching_girls')
'''import scraperwiki
import requests
import csv
import lxml.html

'''
# THE STREET NAME COLLECTION
url = 'http://www.postur.is/gogn/Gotuskra/gotuskra.txt'

response = requests.get(url).text
response = response.encode('iso-8859-1')
print response


reader = csv.reader(response.splitlines(),delimiter=';')
headerline = reader.next()
#reader = csv.DictReader(response.splitlines(),delimiter=';')

data = []

for row in reader:
    x = {}
    x['key'] = row[0].decode('iso-8859-1')
    x['zip'] = row[1].decode('iso-8859-1')
    x['nefnifall'] = row[2].decode('iso-8859-1')
    x['thagufall'] = row[3].decode('iso-8859-1')
    data.append(x)
    
print data

exit()
scraperwiki.sqlite.save(unique_keys=['key'], data=data)
'''



# THE NAME COLLECTION



scraperwiki.sqlite.execute("drop table if exists boys")
scraperwiki.sqlite.execute("drop table if exists girls")

#Boys

url = 'http://www.island.is/islensk-nofn?Stafrof=&Nafn=&Drengir=on&Samthykkt=yes'
response = requests.get(url).text
root = root = lxml.html.fromstring(response)
names = root.xpath('//ul[@class="dir"]/li')
data = []
counter = 1
for x in names:
    if x.text != None:
        record = {}
        record['name'] = x.text.strip()
        record['key'] = counter
        data.append(record)
        counter = counter+1
print data
scraperwiki.sqlite.save(unique_keys=['key'], data=data,table_name='boys')

#Girls

url = 'http://www.island.is/islensk-nofn?Stafrof=&Nafn=&Stulkur=on&Samthykkt=yes'
response = requests.get(url).text
root = root = lxml.html.fromstring(response)
names = root.xpath('//ul[@class="dir"]/li')
data = []
counter = 1
for x in names:
    if x.text != None:
        record = {}
        record['name'] = x.text.strip()
        record['key'] = counter
        data.append(record)
        counter = counter+1
scraperwiki.sqlite.save(unique_keys=['key'], data=data,table_name='girls')


# MATCHING
'''
scraperwiki.sqlite.execute("drop table if exists matching_boys")
scraperwiki.sqlite.execute("drop table if exists matching_girls")

#select only the zipz in reykjavik
streets = scraperwiki.sqlite.select('* from "swdata" where "zip" like "10%" OR "zip" like "116"')

#select the boys and the girls
boys = scraperwiki.sqlite.select("name from boys")
girls = scraperwiki.sqlite.select("name from girls")
boys_names = []
girls_names = []
streets_nefnifall = []

#put streets, boys and girl names into lists
for street in streets:
    streets_nefnifall.append(street['nefnifall'])
for name in boys:
    boys_names.append(name['name'])
for name in girls:
    girls_names.append(name['name'])

#match the boys names agains the streets
matching_boys = []
for name in boys_names:
    match = filter(lambda x: name in x,streets_nefnifall)
    if match != []:
        for x in match:
            record = {}
            record['name'] = name
            record['matching_street'] = x
            matching_boys.append(record)


#match the girls names agains the streets
matching_girls = []
for name in girls_names:
    match = filter(lambda x: name in x,streets_nefnifall)
    if match != []:
        for x in match:
            record = {}
            record['name'] = name
            record['matching_street'] = x
            matching_girls.append(record)

#save the matches into two tables

scraperwiki.sqlite.save(unique_keys=['matching_street'], data=matching_boys,table_name='matching_boys')
scraperwiki.sqlite.save(unique_keys=['matching_street'], data=matching_girls,table_name='matching_girls')
'''