# import urllib
# import mechanize

# url = "http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra"
# url = "http://seagrass.goatchurch.org.uk"

# br = mechanize.Browser()
# No robots
# br.set_handle_robots(False)
# Can sometimes hang without this
# br.set_handle_refresh(False)
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# response = br.open(url)
# print response.read()

# print urllib.urlopen(url).read()

##

import urllib
import urllib2

AGENT = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"

scraper_url = "http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra"
print scraper_url

# Open the connection!
try:
    request = urllib2.Request(scraper_url)
    handle = urllib2.build_opener()
except IOError:
    pass

# Let the server know we are using a "fake" User-Agent
request.add_header("User-Agent", AGENT)

# Successfully connected?
if handle:
    try:
        html = handle.open(request).read()
    except urllib2.HTTPError as error:
        print "[ERROR] HTTPError %d: %s -> %s" % (error.code, error, error.url)
    except urllib2.URLError as error:
        print "[ERROR] URLError: %s" % error

    print unicode(html, "utf-8", errors="ignore")
