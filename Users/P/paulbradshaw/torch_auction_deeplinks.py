import scraperwiki
import lxml.html
import urlparse

# Blank Python

base_url = 'http://memorabilia.london2012.com'
firstpage = '/iSynApp/allAuction.action?rc=20&sid=1100443&pgmode1=allauctions&sort=timeleft_asc&selectedCatId=10901'
startingurl = base_url+firstpage

#HTML of source page
#<div style="float:left;width:118px;">
#<div style="padding:10px 4px 0 0;line-height:13px;height:40px;">

def scrape_deep(root):
    divs = root.cssselect('div[style="padding-top:10px;"]') #grab everything in <div style="padding-top:10px;">
    for div in divs:
        print div.text_content()
        record = {} 
        if len(div):
            record["allhtml"] = div.text_content()
#            hrefs = div.cssselect('div a') # get all the <a> tags 
 #           record["href"] = hrefs[0].attrib.get('href')
  #          divs = div.cssselect('div') # get all the <div>tags within
   #         record["description"] = divs[1].text_content()
    #        record["secondpart"] = divs[2].text_content()
     #       record["currentbid"] = divs[3].text_content()
      #      thispage = root.cssselect("div.pagination li.current") #<li class="current">3</li>
       #     record["listingspage"] = thispage
            scraperwiki.sqlite.save(["allhtml"],record)

def scrape_divs(root):
    divs = root.cssselect('div[style="float:left;width:118px;"]') # get all the <div><a> tags 
    for div in divs:
        print div.text_content()
        if len(div):
            hrefs = div.cssselect('div a') # get all the <a> tags 
            for href in hrefs:
                deeplink = href.attrib.get('href')
                html = scraperwiki.scrape(deeplink)
                root = lxml.html.fromstring(html)
                scrape_deep(root)

def scrape_and_look_for_next_link(startingurl):
    html = scraperwiki.scrape(startingurl)
    print html
    root = lxml.html.fromstring(html)
    scrape_divs(root)
#<div class="pagination"><li><a>
#<li style="padding-left:8px;">
    next_link = root.cssselect("div.pagination li[style='padding-left:8px;'] a")
    print next_link
    if len(next_link):
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

scrape_and_look_for_next_link(startingurl)import scraperwiki
import lxml.html
import urlparse

# Blank Python

base_url = 'http://memorabilia.london2012.com'
firstpage = '/iSynApp/allAuction.action?rc=20&sid=1100443&pgmode1=allauctions&sort=timeleft_asc&selectedCatId=10901'
startingurl = base_url+firstpage

#HTML of source page
#<div style="float:left;width:118px;">
#<div style="padding:10px 4px 0 0;line-height:13px;height:40px;">

def scrape_deep(root):
    divs = root.cssselect('div[style="padding-top:10px;"]') #grab everything in <div style="padding-top:10px;">
    for div in divs:
        print div.text_content()
        record = {} 
        if len(div):
            record["allhtml"] = div.text_content()
#            hrefs = div.cssselect('div a') # get all the <a> tags 
 #           record["href"] = hrefs[0].attrib.get('href')
  #          divs = div.cssselect('div') # get all the <div>tags within
   #         record["description"] = divs[1].text_content()
    #        record["secondpart"] = divs[2].text_content()
     #       record["currentbid"] = divs[3].text_content()
      #      thispage = root.cssselect("div.pagination li.current") #<li class="current">3</li>
       #     record["listingspage"] = thispage
            scraperwiki.sqlite.save(["allhtml"],record)

def scrape_divs(root):
    divs = root.cssselect('div[style="float:left;width:118px;"]') # get all the <div><a> tags 
    for div in divs:
        print div.text_content()
        if len(div):
            hrefs = div.cssselect('div a') # get all the <a> tags 
            for href in hrefs:
                deeplink = href.attrib.get('href')
                html = scraperwiki.scrape(deeplink)
                root = lxml.html.fromstring(html)
                scrape_deep(root)

def scrape_and_look_for_next_link(startingurl):
    html = scraperwiki.scrape(startingurl)
    print html
    root = lxml.html.fromstring(html)
    scrape_divs(root)
#<div class="pagination"><li><a>
#<li style="padding-left:8px;">
    next_link = root.cssselect("div.pagination li[style='padding-left:8px;'] a")
    print next_link
    if len(next_link):
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

scrape_and_look_for_next_link(startingurl)