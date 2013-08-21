import scraperwiki
import mechanize
import re
import lxml.html
import string


search_base_url = 'http://www.rainbowpages.lk/_controller/searchcontroller.php?action=AdvReligiousSearch'

results_base_url = 'http://www.rainbowpages.lk/relgious-search-result.php?page=%s'

results_length = list(range(1,280))

base_html = scraperwiki.scrape(search_base_url)
print base_html

for i in results_length:
    current_page_url = results_base_url % str(i)
    html = scraperwiki.scrape(current_page_url)
    print html

    #scraperwiki.sqlite.save(unique_keys=["header"],data={"id":idx,"header":adHeader,"location": location, "content_url":content_url,"source":"YMU", "lat":latitude, "lon": longitude, "thumbnail_url":thumbnailUrl})

print "completed scrapping"

