import scraperwiki
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html


def do_scrape():
    az_html = scraperwiki.scrape('http://www.lambeth.gov.uk/Services/')
    list_root = lxml.html.fromstring(az_html)
    for a in list_root.cssselect("div.AZ li a"):
        try:
            page_title =  a.text
            page_link = 'http://www.lambeth.gov.uk' +  a.get('href')

            print "scraping " + page_link 
            page_full_html = scraperwiki.scrape(page_link)
            page_root = lxml.html.fromstring(page_full_html)

            #pull out the section details
            print page_root.cssselect('div.breadCrumb a')[2].text
            sections_csv = page_root.cssselect('div.breadCrumb a')[2].text

            #check it is a content page, not a nav page
            if page_full_html.find('cScape.Lambeth.GenericTemplates/ServiceCategory.aspx') <0 and page_full_html.find('cScape.Lambeth.GenericTemplates/DocumentSummary.aspx') <0 and page_full_html.find('cScape.Lambeth.GenericTemplates/GroupDocument.aspx') <0:

                content_fragment = page_root.cssselect('div.page')[0]
                for toplink in content_fragment.cssselect('div.topLink'):
                    content_fragment.remove(toplink)
                content_html = lxml.html.tostring(content_fragment)  
                content_html = clean_html(content_html)


                scraperwiki.sqlite.save(unique_keys=["source_url"], data={"source_url":page_link, "title":page_title, "content": content_html, 'sections_csv': sections_csv})
            else:
                print "ignoring nav page"
        except:
            print "something went wrong"
            pass


do_scrape()