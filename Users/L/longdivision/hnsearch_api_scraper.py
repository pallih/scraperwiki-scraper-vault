import json
import string

import scraperwiki

id = scraperwiki.sqlite.get_var('last_id')
apiurl = "http://hndroidapi.appspot.com/post/format/json/id/"
apiurlparams = "?appid=HNOnScraperWiki"
scrape = True

while scrape:
    url = apiurl + str(id) + apiurlparams
    try:
        html = scraperwiki.scrape(url)
        # strip out control chars
        html = html.translate(string.maketrans("\n\r\t", "   "))
        html = unicode(html)
    except:
        # repeat request for the same id
        break
    data = json.loads(html)

    print data
    # excluse comments (empty list) and ads (which don't have an item_id)
    if not data['items'] or not ('item_id' in data['items'][0]): 
        print "Item", str(id), "not a post."
    else:
        item = data['items'][0]
        print "Saving item", str(id)
        print item
        scraperwiki.sqlite.save(unique_keys=['item_id'], data=item)

    scraperwiki.sqlite.save_var('last_id', id)
    id += 1

    # The API will return results similar to a comment even for IDs which don't exist yet
    # This arbitrary recent id is used to stop the run
    # Not currently important as there are millions posts to be scraped yet
    if id > 5334905: 
        scrape = False

