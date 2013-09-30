import json
import urllib


url='http://www.hackruiter.com/companies.json'
f = urllib.urlopen(url)
data = json.loads(f.read())


# new practice: what are we dealing with? Ask!
print type(data)
print len(data)

#print json.dumps(data, s indent=4 * ' ')

for item in data:
   # print type(item)
    print len(item)
    print item.keys()
    print item.values()
    for entry in item.values():
        print entry;

# scraperwiki.datastore.save(["establishmentNumber"], record)
import json
import urllib


url='http://www.hackruiter.com/companies.json'
f = urllib.urlopen(url)
data = json.loads(f.read())


# new practice: what are we dealing with? Ask!
print type(data)
print len(data)

#print json.dumps(data, s indent=4 * ' ')

for item in data:
   # print type(item)
    print len(item)
    print item.keys()
    print item.values()
    for entry in item.values():
        print entry;

# scraperwiki.datastore.save(["establishmentNumber"], record)
