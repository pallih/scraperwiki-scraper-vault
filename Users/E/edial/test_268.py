import scraperwiki           
import lxml.html
import urllib2
import urllib

print "Starting"

url = "http://www.britainsbestguides.org/search-results/"
header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=fbed5d732ae60a57f39040f3dc1fefcc; __utma=204497347.1684001878.1342267933.1342267933.1342267933.1; __utmb=204497347.2.10.1342267933; __utmc=204497347; __utmz=204497347.1342267933.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)' }

req = urllib2.Request(url, None, header)  
response = urllib2.urlopen(req)

print "Parsing"

root = lxml.html.fromstring(response.read())

for el in root.cssselect("#body div div div div div p a"): 
    page_url = "http://www.britainsbestguides.org" + el.get("href");
    print page_url  
    page_html = scraperwiki.scrape(page_url) 
    page = lxml.html.fromstring(page_html)
    name = page.cssselect("#body #profile_col1 table tr:nth-of-type(1) td.col2 p")
    print name[0].text_content()
    
    tel = page.cssselect("#body #profile_col1 table tr:nth-of-type(2) td.col2 p")
    print tel[0].text_content()

    email = page.cssselect("#body #profile_col1 table tr:nth-of-type(3) td.col2 p")
    print email[0].text_content()

        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        scraperwiki.sqlite.save(unique_keys=['tel'], data=data)
        scraperwiki.sqlite.save(unique_keys=['email'], data=data)