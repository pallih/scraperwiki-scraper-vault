# Blank Python
#
# categorylist ["farming", "Animals-Livestock", "baby-goods", "entertianment", "business", "clothes", "collectibles", "computers", "diy",
# "electicals", "furniture", "health-and-fitness", "house-and-home", "jewellery", "lostandfound", "miscellaneous", "mobile-phones",
# "boats", "cars", "motorbikes", "music-equipment", "properties", "sports-equipment", "toys", "travel", "wanted", "weddings"]
# NOTE Apparent typos above are accurate!

#example url 'http://www.manx.net/classifieds/mobile-phones/advert/110838'
#PROBLEM #1 Advert numbers appear sequential, but not within each category. So this will be a 'noisy' search unless we can deal with this.
#SOLUTION? Possible help from this page 'http://www.manx.net/Classifieds' this lists the ten most recent additions and their urls.
#
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.manx.net/classifieds/mobile-phones/advert/110838'

html = scraperwiki.scrape(starting_url)
print html
#soup = beautifulsoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
#
# Blank Python
#
# categorylist ["farming", "Animals-Livestock", "baby-goods", "entertianment", "business", "clothes", "collectibles", "computers", "diy",
# "electicals", "furniture", "health-and-fitness", "house-and-home", "jewellery", "lostandfound", "miscellaneous", "mobile-phones",
# "boats", "cars", "motorbikes", "music-equipment", "properties", "sports-equipment", "toys", "travel", "wanted", "weddings"]
# NOTE Apparent typos above are accurate!

#example url 'http://www.manx.net/classifieds/mobile-phones/advert/110838'
#PROBLEM #1 Advert numbers appear sequential, but not within each category. So this will be a 'noisy' search unless we can deal with this.
#SOLUTION? Possible help from this page 'http://www.manx.net/Classifieds' this lists the ten most recent additions and their urls.
#
import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.manx.net/classifieds/mobile-phones/advert/110838'

html = scraperwiki.scrape(starting_url)
print html
#soup = beautifulsoup(html)

# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
#
