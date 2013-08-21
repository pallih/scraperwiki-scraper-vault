#Scrape Green Party Press Releases
import scraperwiki
import lxml.html


pagename = 'http://www.gp.org/press.php'
#Scrape the page
page = scraperwiki.scrape(pagename)
#Root the page
pageroot = lxml.html.fromstring(page)
for link in pageroot.cssselect('''span.PRHeadline a'''): 
    docpagename = link.attrib['href']
    docpage = scraperwiki.scrape('http://www.gp.org/' + docpagename)
    docpageroot = lxml.html.fromstring(docpage)    
    document = docpageroot.text_content()
    data = {'Document': document}
    scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)
#Scrape Green Party Press Releases
import scraperwiki
import lxml.html


pagename = 'http://www.gp.org/press.php'
#Scrape the page
page = scraperwiki.scrape(pagename)
#Root the page
pageroot = lxml.html.fromstring(page)
for link in pageroot.cssselect('''span.PRHeadline a'''): 
    docpagename = link.attrib['href']
    docpage = scraperwiki.scrape('http://www.gp.org/' + docpagename)
    docpageroot = lxml.html.fromstring(docpage)    
    document = docpageroot.text_content()
    data = {'Document': document}
    scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)
