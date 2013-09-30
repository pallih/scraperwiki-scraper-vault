import lxml.html
import lxml.etree        
import scraperwiki


#artist = 'Cher'
artist = 'MSE+Artist+1'
api_key = 'afbaa3422539aef6f6cf3114a32968c3'


url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getevents&artist=' + artist + '&api_key=' + api_key

html = scraperwiki.scrape(url)
root = lxml.etree.fromstring(html)
events = root.xpath('/lfm/events/event')

for event in events:
    id = event[0].text
    title = event[1].text
    data = {
        'event_id': id,
        'artist': artist,
        'title': title
    }
    scraperwiki.sqlite.save(unique_keys=['event_id'], data=data)



# for tr in root.cssselect("table[class='candyStriped chart'] tbody tr"):
#    tds = tr.cssselect("td")
#    data = {
#      'artist' : tds[2].text_content().replace("\n", "").strip(" "),
#      'scrobbles' : int(tds[5].text_content().replace(",", "").strip("\n").strip(" "))
#    }
#    scraperwiki.sqlite.save(unique_keys=['artist'], data=data)import lxml.html
import lxml.etree        
import scraperwiki


#artist = 'Cher'
artist = 'MSE+Artist+1'
api_key = 'afbaa3422539aef6f6cf3114a32968c3'


url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getevents&artist=' + artist + '&api_key=' + api_key

html = scraperwiki.scrape(url)
root = lxml.etree.fromstring(html)
events = root.xpath('/lfm/events/event')

for event in events:
    id = event[0].text
    title = event[1].text
    data = {
        'event_id': id,
        'artist': artist,
        'title': title
    }
    scraperwiki.sqlite.save(unique_keys=['event_id'], data=data)



# for tr in root.cssselect("table[class='candyStriped chart'] tbody tr"):
#    tds = tr.cssselect("td")
#    data = {
#      'artist' : tds[2].text_content().replace("\n", "").strip(" "),
#      'scrobbles' : int(tds[5].text_content().replace(",", "").strip("\n").strip(" "))
#    }
#    scraperwiki.sqlite.save(unique_keys=['artist'], data=data)