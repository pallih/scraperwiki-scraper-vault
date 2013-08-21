import scraperwiki
import lxml.html
#
# The scrip extract the links to scraper raw code and 
# returns the links that can be paste into download manager
#



# Paste here your home url
home_url=url="https://scraperwiki.com/profiles/slava/"

while url!='':

    html=scraperwiki.scrape(url)
    root=lxml.html.document_fromstring(html)
    for el in root.xpath('//*[@id="content"]/ul/li/h3/a[2]'):
        scraper_link=el.attrib['href']
        if scraper_link.find('/scrapers/') != -1:
            scraper_link='https://scraperwiki.com/' + scraper_link.replace('/scrapers/', 'editor/raw/')
            print scraper_link.rstrip('/')

    next_url=root.xpath('//*[@class="pagination"]/*[@class="next"]')
    if next_url != []:
        url=home_url + next_url[0].attrib['href']
    else:
        url=''
