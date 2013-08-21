import scraperwiki
import urllib2
import lxml.etree
import lxml.html


# get list fo all pdfs to scrape:
#http://www.london-gazette.co.uk/issues/1960-01-01;2012-11-01/exact=licence+to+abstract+water;sort=oldest/start=1
#http://www.london-gazette.co.uk/issues/1960-01-01;2012-11-01/exact=licence+to+abstract+water;sort=oldest/start=16752

#for i in range(1,16753):
record={}
#n=0
n=5616
#12251 #example of both types
#for i in range(1,16753,10):
#for i in range(561,16753,10):
for i in range(5311,16753,10):
    scraperwiki.sqlite.save_var('last_page', i)
    url = "http://www.london-gazette.co.uk/issues/1960-01-01;2012-11-01/exact=licence+to+abstract+water;sort=oldest/start=%s" % i
    #html=scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)  
    root=lxml.html.fromstring(scraperwiki.scrape(url))
    ax =root.cssselect('li.lteIE6_first-child a')
    for a in ax:
        n=n+1
        if a.attrib['typeof'] in 'g:Notice' : #link to notice exists
            record={}
            record['page_id']=i        
            record['id']=n    
            record['sourceurl']=url
            record['link']=a.attrib['about']
            scraperwiki.sqlite.save(['link'], record, 'websites')
        else: #only link to pdf
            record={}
            record['page_id']=i
            record['id']=n    
            record['sourceurl']=url
            record['pdflink']='http://www.london-gazette.co.uk' + a.attrib['href'] + '/page.pdf'
            scraperwiki.sqlite.save(['pdflink'], record, 'pdfs')
        
    #print scraperwiki.scrape(url)