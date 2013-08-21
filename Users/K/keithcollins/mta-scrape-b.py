# from keith: if anyone can get this to load subsequent pages and output html,
# i would suggest saving the html pages locally with iterated number suffixes, 
# then scraping those local html pages.
import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://archive.mymtaalerts.com/messagearchive.aspx'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(10):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    # from keith: prints all html on page. would be better to save the html pages locally.
    print html

    # from keith: seems this was put here to check if on last page. always evaluates false so i took it out.
    #mnextlink = re.search("javascript:__doPostBack\('RadGrid1$ctl00$ctl03$ctl01$ctl05',''\).>/<span/>1/<//span/>", html)    
    #if not mnextlink:
        #break
    
    # from keith: this should load the next page but it doesn't
    # the RadGrid string changes on some pages
    br.select_form(name='form1')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'RadGrid1$ctl00$ctl03$ctl01$ctl26'
    br['__EVENTARGUMENT'] = ' '
    response = br.submit()

