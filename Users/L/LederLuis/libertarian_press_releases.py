# Scrape the GOP press releases

import scraperwiki
import lxml.html


#Find number of pages to scrape
npages = 65

counter = 0

# Make list of links
for i in range(0, npages+1):
    # Concatenate integer with base to make pagename
    pagename = 'http://www.lp.org/news?page=' + str(i)
    #Scrape the page
    page = scraperwiki.scrape(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('''div#content-area a'''):
        docpagename = link.attrib['href']
        if docpagename[0:6] == '/news/':
            docpage = scraperwiki.scrape('http://www.lp.org' + docpagename)
        else:
            if docpagename[11:22] != 'lp.org/news':
                continue
            else:
                docpage = scraperwiki.scrape(docpagename)
        docpageroot = lxml.html.fromstring(docpage)
        for d in docpageroot.cssselect('div.node'):
            doc = d.text_content()   
            cleantext = doc.replace('For Immediate Release', '')
            data = {'Document': cleantext}
            scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)
    
    