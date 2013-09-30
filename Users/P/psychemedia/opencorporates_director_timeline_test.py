# Blank Python
import simplejson, urllib

sourcescraper = ''
print "<html><head><title></title></head><body>"

print "<table>"

url="http://api.opencorporates.com/v0.2/companies/gb/00102498"

data=simplejson.load(urllib.urlopen(url))

for officer in data['results']['company']['officers']:
    director=officer["officer"]
    if director["start_date"]==None: director["start_date"]=''
    if director["end_date"]==None: director["end_date"]=''
    print "<tr><td>"+str(director["id"])+"</td><td>"+director["position"]+"</td><td>"+director["name"]+"</td><td>"+director["start_date"]+"</td><td>"+director["end_date"]+"</td></tr>"


print "</table>"

print "</body></html>"# Blank Python
import simplejson, urllib

sourcescraper = ''
print "<html><head><title></title></head><body>"

print "<table>"

url="http://api.opencorporates.com/v0.2/companies/gb/00102498"

data=simplejson.load(urllib.urlopen(url))

for officer in data['results']['company']['officers']:
    director=officer["officer"]
    if director["start_date"]==None: director["start_date"]=''
    if director["end_date"]==None: director["end_date"]=''
    print "<tr><td>"+str(director["id"])+"</td><td>"+director["position"]+"</td><td>"+director["name"]+"</td><td>"+director["start_date"]+"</td><td>"+director["end_date"]+"</td></tr>"


print "</table>"

print "</body></html>"