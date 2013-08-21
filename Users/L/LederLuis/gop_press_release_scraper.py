# Scrape the GOP press releases

import scraperwiki
import lxml.html


#Find number of pages to scrape
home = scraperwiki.scrape('http://www.gop.com/news/press-releases/')
homeroot = lxml.html.fromstring(home)
pagenumber = homeroot.cssselect('div.vieopost-pagination')
pagenumbertext = pagenumber[0].text
npageslist = pagenumbertext.split(' ')
npageslist = [i for i in npageslist if i is not '']
npages = int(npageslist[-1])

pagenames = []
links = []
docs = []



# Make list of links
for i in range(1, npages+1):
    # Concatenate integer with base to make pagename
    pagename = 'http://www.gop.com/news/press-releases/page/' + str(i) + '/'
    #Scrape the page
    page = scraperwiki.scrape(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('''div.'vieopost-title recent-title' a'''):    
        docpagename = link.attrib['href']
        if docpagename == 'http://www.gop.com/news/press-releases/15041/':
            continue
        docpage = scraperwiki.scrape(docpagename)
        docpageroot = lxml.html.fromstring(docpage)
        for d in docpageroot.cssselect('div.vieopost-body'):
            doc = d.text_content()
            #GOP uses # at end of docs
            cleandoc = doc.replace("#", "")
            #Grab document name
            docname = docpagename.split('/')[-1]
        for t in docpageroot.cssselect('div.vieopost-post-date'):
            date = t.text_content()
        data = {'Date': date,'Document': docname + ' '+ cleandoc}
        scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)


# Scrape the GOP press releases

import scraperwiki
import lxml.html


#Find number of pages to scrape
home = scraperwiki.scrape('http://www.gop.com/news/press-releases/')
homeroot = lxml.html.fromstring(home)
pagenumber = homeroot.cssselect('div.vieopost-pagination')
pagenumbertext = pagenumber[0].text
npageslist = pagenumbertext.split(' ')
npageslist = [i for i in npageslist if i is not '']
npages = int(npageslist[-1])

pagenames = []
links = []
docs = []



# Make list of links
for i in range(1, npages+1):
    # Concatenate integer with base to make pagename
    pagename = 'http://www.gop.com/news/press-releases/page/' + str(i) + '/'
    #Scrape the page
    page = scraperwiki.scrape(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('''div.'vieopost-title recent-title' a'''):    
        docpagename = link.attrib['href']
        if docpagename == 'http://www.gop.com/news/press-releases/15041/':
            continue
        docpage = scraperwiki.scrape(docpagename)
        docpageroot = lxml.html.fromstring(docpage)
        for d in docpageroot.cssselect('div.vieopost-body'):
            doc = d.text_content()
            #GOP uses # at end of docs
            cleandoc = doc.replace("#", "")
            #Grab document name
            docname = docpagename.split('/')[-1]
        for t in docpageroot.cssselect('div.vieopost-post-date'):
            date = t.text_content()
        data = {'Date': date,'Document': docname + ' '+ cleandoc}
        scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)


