import scraperwiki
urlstart = 'http://discovery.nationalarchives.gov.uk/SearchUI/s/res/'
urlend = '1?_aq=*&_ro=any&_cs=D&_rv=simple&_advtxt=*&_ps=60'

for i in range(3700):
    urlmiddle = str(i)
    url = urlstart + urlmiddle + urlend
    html = scraperwiki.scrape(url)
    import lxml.html
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    anchors = root.cssselect('a.linkTitle') # get all the <span> tags with description as class
    for a in anchors:
     line = a.text                # just the text inside the HTML tag
     record = { "a" : line } # column name and value
     scraperwiki.sqlite.save(["a"], record) # save the records one by one
    print "Hello", i
    

