import scraperwiki

# Blank Python
import urllib
print urllib.urlopen('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=civic_commons_extracting_links_of_all_apps&query=select%20*%20from%20%60army_ants_civic_commons_apps%60%20').read()
