from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

URL = "http://www.skagitcounty.net/jail/HTML/jailbooking.xml"

page = urlopen(URL)
xml = page.read()

currenttime = datetime.datetime.now()
save(['xml'], {"xml":xml, "date-scraped":currenttime}, 'raw-files')from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

URL = "http://www.skagitcounty.net/jail/HTML/jailbooking.xml"

page = urlopen(URL)
xml = page.read()

currenttime = datetime.datetime.now()
save(['xml'], {"xml":xml, "date-scraped":currenttime}, 'raw-files')