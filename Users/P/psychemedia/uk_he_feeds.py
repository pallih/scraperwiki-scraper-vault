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

sourcescraper = 'uk_university_autodiscoverable_rss_feeds'
scraperwiki.sqlite.attach(sourcescraper) 
print "<html><head><title>UK Autodiscoverable Feeds</title></head>"
print "<body>"
done=[]

hecount=scraperwiki.sqlite.select('feeds from `'+sourcescraper+'`.hecountdata')
feedcount=scraperwiki.sqlite.select('feeds from `'+sourcescraper+'`.hecountdata WHERE feeds>0')
heicnt=len(hecount)
fcnt=len(feedcount)
fhr=(100*len(feedcount))/len(hecount)
print "HEIs:",heicnt,'Feeds:',fcnt,'Percentage w/ autodiscoverable feeds:',fhr
header('h2','UK HE News Feeds')
news=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%news%" OR feed LIKE "%news%"')
tabulate(news)

done=newitem(done,news)

header('h2','UK HE Events Feeds')
events=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%event%" OR feed LIKE "%event%"')
tabulate(events)

done=newitem(done,events)

header('h2','UK HE Research Feeds')
research=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%research%" OR feed LIKE "%research%"')
tabulate(research)

done=newitem(done,research)

header('h2','UK HE Jobs Feeds')
jobs=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%job%" OR furl LIKE "%career%" OR furl LIKE "%vacanc%" OR furl LIKE "%recruit%" OR feed LIKE "%job%" OR feed LIKE "%career%" OR feed LIKE "%vacanc%" OR feed LIKE "%recruit%" OR feed LIKE "%working%"')
tabulate(jobs)

done=newitem(done,jobs)

header('h2','UK HE Twitter Feeds')
twitter=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%twitter.co%"')
tabulate(twitter)

done=newitem(done,twitter)

header('h2','UK HE YouTube Feeds')
youtube=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%youtube.co%" ')
tabulate(youtube)

done=newitem(done,youtube)

other=[]

header('h2','UK HE Other Feeds')
all=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata')
for i in all:
    if i['furl'] not in done:
        other.append(i)
tabulate(other)

print "</body></html>"import scraperwiki
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

sourcescraper = 'uk_university_autodiscoverable_rss_feeds'
scraperwiki.sqlite.attach(sourcescraper) 
print "<html><head><title>UK Autodiscoverable Feeds</title></head>"
print "<body>"
done=[]

hecount=scraperwiki.sqlite.select('feeds from `'+sourcescraper+'`.hecountdata')
feedcount=scraperwiki.sqlite.select('feeds from `'+sourcescraper+'`.hecountdata WHERE feeds>0')
heicnt=len(hecount)
fcnt=len(feedcount)
fhr=(100*len(feedcount))/len(hecount)
print "HEIs:",heicnt,'Feeds:',fcnt,'Percentage w/ autodiscoverable feeds:',fhr
header('h2','UK HE News Feeds')
news=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%news%" OR feed LIKE "%news%"')
tabulate(news)

done=newitem(done,news)

header('h2','UK HE Events Feeds')
events=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%event%" OR feed LIKE "%event%"')
tabulate(events)

done=newitem(done,events)

header('h2','UK HE Research Feeds')
research=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%research%" OR feed LIKE "%research%"')
tabulate(research)

done=newitem(done,research)

header('h2','UK HE Jobs Feeds')
jobs=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%job%" OR furl LIKE "%career%" OR furl LIKE "%vacanc%" OR furl LIKE "%recruit%" OR feed LIKE "%job%" OR feed LIKE "%career%" OR feed LIKE "%vacanc%" OR feed LIKE "%recruit%" OR feed LIKE "%working%"')
tabulate(jobs)

done=newitem(done,jobs)

header('h2','UK HE Twitter Feeds')
twitter=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%twitter.co%"')
tabulate(twitter)

done=newitem(done,twitter)

header('h2','UK HE YouTube Feeds')
youtube=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata WHERE furl LIKE "%youtube.co%" ')
tabulate(youtube)

done=newitem(done,youtube)

other=[]

header('h2','UK HE Other Feeds')
all=scraperwiki.sqlite.select('* from `'+sourcescraper+'`.swdata')
for i in all:
    if i['furl'] not in done:
        other.append(i)
tabulate(other)

print "</body></html>"