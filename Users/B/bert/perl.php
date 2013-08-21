import urllib
import urlparse
import re

url = "http://curl.haxx.se/mail/list.cgi?list=curl-and-php"
html = urllib.urlopen(url).read()
for  name in re.findall('<a
href="(/~.*?/)"><b>(.*?)</b></a><br/><small>(.*?)</small>', html):
    alk = urlparse.urljoin(url, lk)

    data = {  'name':name }

    phtml = urllib.urlopen(alk).read()
    memail = re.search('<a href="mailto:(.*?)">', phtml)
    if memail:
        data['email'] = memail.group(1)

    print data 




