import scraperwiki
import lxml.html
import re
import urllib2

html = scraperwiki.scrape("http://www.catprotection.org.au/cats-available-for-adoption")

root = lxml.html.fromstring(html)
for cat in root.cssselect("div.cats_list_bottom"):

    detail_url = cat.cssselect("a")[1].get("href");
    img = cat.cssselect("img")[0].get("src");

    detail_html = scraperwiki.scrape(detail_url);
    detail = lxml.html.fromstring(detail_html).cssselect("div.port_info")[0];
    
# The kittens page is a constant bogus entry, it doesn't have a sex entry, so need to skip it.
# Kittens page: http://www.catprotection.org.au/cats-available-for-adoption?secid=1&catid=2&task=fullview&id=94
    if (detail.cssselect("tr")[0].cssselect("td")[1].text_content() == 'kittens'):
        continue

# This could be easily changed to look at the first TD in a row and dynamically determine the category to make it more robust, but I don't know yet what other categories pet adoption sites use.
    data = {
         'id'    : int(re.search('(?<=&id=).+',detail_url).group(0))
# We are able to infer when a cat was added by the date their thumbnail was created.
# Scraperwiki should make it easier to access headers through the scraperwiki header object.    
        ,'create_date' : urllib2.urlopen(img).info()['Last-Modified']
        ,'img'   : img
        ,'more_info' : detail_url
        ,'name'  : detail.cssselect("tr")[0].cssselect("td")[1].text_content()
        ,'sex'   : detail.cssselect("tr")[1].cssselect("td")[1].text_content()
        ,'breed' : detail.cssselect("tr")[2].cssselect("td")[1].text_content()
        ,'age'   : detail.cssselect("tr")[3].cssselect("td")[1].text_content()
        ,'description' : detail.cssselect("tr")[4].cssselect("td")[1].text_content()
        ,'colour': detail.cssselect("tr")[5].cssselect("td")[1].text_content()
        ,'home'  : detail.cssselect("tr")[6].cssselect("td")[1].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)


