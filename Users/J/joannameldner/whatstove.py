      
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/stove-reviews.html") 
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any")

#www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any
# ...
#www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any

import scraperwiki
import lxml.html

#list of all pages to scrape:
urllist = [
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=3&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=4&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=5&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=6&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=7&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=8&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=9&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any'
];

#create repeatable scraper routine, to do each page
def scrape_urls(html):
    root = lxml.html.fromstring(html)
    ax = root.cssselect('div.jr_tableview a') # get all the <a> tags
    for a in ax:
            record = {}
            #print lxml.html.tostring(a)
            #record['link']=a.attrib['href']
            #scraperwiki.sqlite.save(['link'], record) # save the records one by one
            s=a.attrib['href']
            if s.find("#") == -1:
                record['link']='http://www.whatstove.co.uk' + a.attrib['href']
                scraperwiki.sqlite.save(['link'], record)
      

#set variable
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any")
#html=scraperwiki.scrape(urllist[1])

#call routine
#scrape_urls(html)

for link in urllist:
    html=scraperwiki.scrape(link)
    scrape_urls(html)
    




























          
    
#trs = root.cssselect('div.jr_tableview tr') # get all the <tr> tags

##for tr in trs:
##    print lxml.html.tostring(tr) # the full HTML tag
##    print tr.text                # just the text inside the HTML tag

#for tr in trs:
#    tds=tr.cssselect('td')
#    for td in tds:
#        record = {}
#        print a
#        print td.attrib['class']
#        print lxml.html.tostring(td)
#        record['id']=a
#        record['order']=td.attrib['class']
#        record['value']=lxml.html.tostring(td)
#        #record = { td.attrib['class'] : lxml.html.tostring(td) } # column name and value
#        a=a+1 
#        scraperwiki.sqlite.save(['id'], record) # save the records one by one


#for tr in trs: 
#    td1=tr.cssselect('td.columnFirst a')
#    for a in td1:  
#        print lxml.html.tostring(td1)


      
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/stove-reviews.html") 
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any")

#www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any
# ...
#www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any

import scraperwiki
import lxml.html

#list of all pages to scrape:
urllist = [
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=3&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=4&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=5&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=6&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=7&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=8&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=9&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any'
];

#create repeatable scraper routine, to do each page
def scrape_urls(html):
    root = lxml.html.fromstring(html)
    ax = root.cssselect('div.jr_tableview a') # get all the <a> tags
    for a in ax:
            record = {}
            #print lxml.html.tostring(a)
            #record['link']=a.attrib['href']
            #scraperwiki.sqlite.save(['link'], record) # save the records one by one
            s=a.attrib['href']
            if s.find("#") == -1:
                record['link']='http://www.whatstove.co.uk' + a.attrib['href']
                scraperwiki.sqlite.save(['link'], record)
      

#set variable
#html =  scraperwiki.scrape("http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any")
#html=scraperwiki.scrape(urllist[1])

#call routine
#scrape_urls(html)

for link in urllist:
    html=scraperwiki.scrape(link)
    scrape_urls(html)
    




























          
    
#trs = root.cssselect('div.jr_tableview tr') # get all the <tr> tags

##for tr in trs:
##    print lxml.html.tostring(tr) # the full HTML tag
##    print tr.text                # just the text inside the HTML tag

#for tr in trs:
#    tds=tr.cssselect('td')
#    for td in tds:
#        record = {}
#        print a
#        print td.attrib['class']
#        print lxml.html.tostring(td)
#        record['id']=a
#        record['order']=td.attrib['class']
#        record['value']=lxml.html.tostring(td)
#        #record = { td.attrib['class'] : lxml.html.tostring(td) } # column name and value
#        a=a+1 
#        scraperwiki.sqlite.save(['id'], record) # save the records one by one


#for tr in trs: 
#    td1=tr.cssselect('td.columnFirst a')
#    for a in td1:  
#        print lxml.html.tostring(td1)


