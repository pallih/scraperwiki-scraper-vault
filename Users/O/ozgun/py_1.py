# Blank Python
sourcescraper = 'py'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(
    '''* from swdata 
    '''
)

channel=""

tags = {"NATGEO":"national geographic", "Kanal D":"@kanald", "Star":"@startv", "CNBC-E":"@cnbce", "Show":"@showtv", "TRT1":"trt", "TV 8":"@tv8", "Atv":"atv"}

print "<table>"           
print "<tr><th>Date</th><th>Channel</th><th>Title</th><th>tag</th><th>StartH</th><th>StartM</th>"
for d in data:
    if d["Channel"].strip() != channel:
        print "<tr><td>-</td><td></td><td></td><td></td></tr>"    
        print "<tr><td>-</td><td></td><td></td><td></td></tr>"    
        print "<tr><td>-</td><td></td><td></td><td></td></tr>"    
        print "<tr><td>-</td><td></td><td></td><td></td></tr>"    

    channel = d["Channel"].strip()
    print "<tr>"
    print "<td>"+d["Date"].strip()+"</td>"
    print "<td>"+d["Channel"].strip()+"</td>"
    print "<td>"+d["Title"].strip()+"</td>"
    print "<td>"+tags[channel].strip()+"</td>"
    print "<td>"+str(d["StartH"])+"</td>"
    print "<td>"+str(d["StartM"])+"</td>"
    print "</tr>"
print "</table>"
