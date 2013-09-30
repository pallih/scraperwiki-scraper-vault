#This is a script for pulling the comments from an age article. It only looks at a specific article at the moment, might change this to scan for relvant articles in the future.
import lxml.html
import scraperwiki
html=scraperwiki.scrape("http://www.theage.com.au/it-pro/business-it/nab-internet-banking-site-goes-down-20120905-25dbp.html")
#Step one, get the id for the more-comments page
doc = lxml.html.document_fromstring(html)
tmp = list()
for elem in doc.iter():
    if elem.tag == 'a':
        for ii in elem.items():
            if (ii[0].lower() == 'data-assetid'):
                tmp.append(elem)
urlInsert= tmp[0].items()[1][1]
newUrL="http://www.theage.com.au/ugc/moreComments.ajax?assetId=" + urlInsert + "&type=comments"
print newUrL

           
#Step 2, get the more comments, and get the data!
html=scraperwiki.scrape(newUrL)
print html
root = lxml.html.fromstring(html)
x=0
for li in root:
    tds = li.cssselect("blockquote")
    data = {
        'Comments' : tds[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['Comments'], data=data)

            
# <p class="more-comments"><span><a href="javascript:;" data-assetId=d-25dbp>More comments</a></span></p>
#This is a script for pulling the comments from an age article. It only looks at a specific article at the moment, might change this to scan for relvant articles in the future.
import lxml.html
import scraperwiki
html=scraperwiki.scrape("http://www.theage.com.au/it-pro/business-it/nab-internet-banking-site-goes-down-20120905-25dbp.html")
#Step one, get the id for the more-comments page
doc = lxml.html.document_fromstring(html)
tmp = list()
for elem in doc.iter():
    if elem.tag == 'a':
        for ii in elem.items():
            if (ii[0].lower() == 'data-assetid'):
                tmp.append(elem)
urlInsert= tmp[0].items()[1][1]
newUrL="http://www.theage.com.au/ugc/moreComments.ajax?assetId=" + urlInsert + "&type=comments"
print newUrL

           
#Step 2, get the more comments, and get the data!
html=scraperwiki.scrape(newUrL)
print html
root = lxml.html.fromstring(html)
x=0
for li in root:
    tds = li.cssselect("blockquote")
    data = {
        'Comments' : tds[0].text_content(),
    }
    scraperwiki.sqlite.save(unique_keys=['Comments'], data=data)

            
# <p class="more-comments"><span><a href="javascript:;" data-assetId=d-25dbp>More comments</a></span></p>
