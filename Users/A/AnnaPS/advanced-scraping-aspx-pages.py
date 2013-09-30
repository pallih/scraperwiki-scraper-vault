import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://recognition.ncqa.org/PSearchResults.aspx?state=NY&rp='
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(10):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

    mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
    if not mnextlink:
        break

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://recognition.ncqa.org/PSearchResults.aspx?state=NY&rp='
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(10):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

    mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
    if not mnextlink:
        break

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

