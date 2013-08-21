import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from time import strptime, strftime, gmtime
from cgi import escape

def header(style,heading):
    print "<"+style+">"+heading+"</"+style+">\n"

def tableset():
    print "<table>\n"

def tablerow(row):
    print "  <tr>\n"
    for j in row:
        print "    <td>"+j+"</td>\n"
    print "  </tr>\n"

def tableunset():
    print "</table>\n"

def tabulate(data):
    tableset()
    for i in data:
        tablerow([i['feed'],i['furl']])
    tableunset()

def newitem(done,items):
    for item in items:
        if 'furl' in item:
            done.append(item['furl'])
    return done

sourcescraper = 'scijobs'
scraperwiki.sqlite.attach(sourcescraper) 
print "<html><head><title>UK JoBrodie/SciJobs Autodiscoverable Feeds</title></head>"
print "<body>"

print "<h1>Scraped and autodetected feeds based on <a href='http://brodiesnotes.blogspot.com/2009/07/amrc-member-charities-websites.html'>@jobrodies scicomm orgs list</a>"

done=[]

header('h2','UK SciComm News Feeds')
news=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%news%" OR feed LIKE "%news%"')
tabulate(news)
done=newitem(done,news)

header('h2','UK SciComm Jobs Feeds')
jobs=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%job%" OR furl LIKE "%career%" OR furl LIKE "%vacanc%" OR furl LIKE "%recruit%" OR feed LIKE "%job%" OR feed LIKE "%career%" OR feed LIKE "%vacanc%" OR feed LIKE "%recruit%" OR feed LIKE "%working%"')
tabulate(jobs)
done=newitem(done,jobs)

header('h2','UK SciComm Events Feeds')
events=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%event%" OR feed LIKE "%event%"')
tabulate(events)
done=newitem(done,events)


other=[]
header('h2','UK SciComm Other Feeds')
all=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata')
for i in all:
    if i['furl'] not in done:
        other.append(i)
tabulate(other)


print "</body></html>"