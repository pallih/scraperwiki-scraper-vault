import scraperwiki
import lxml.html
import dateutil.parser

"""
Example event element: 

<div class="eventDisplay"><div class="eventHeader"><span class="eventName"><a href="
        http://store-locator.barnesandnoble.com/event/4430014">Storytime With Miss Ann</a></span><br><span class="productInfoList"><a href="
        http://store-locator.barnesandnoble.com/event/4430014"></a></span><span class="productTitle"><a href="
        http://store-locator.barnesandnoble.com/event/4430014">Hooray for You! A Celebration of "You-Ness"</a></span></div><span class="eventDetails">Storytime (Children's)</span><br><span class="eventTime">Wednesday July 03, 2013&nbsp;10:30 AM </span><br><a class="smallImage rArrow" href="
        http://store-locator.barnesandnoble.com/event/4430014"><b>More about this event</b></a></div>
"""
def get_text(cssselector): 
    return el.cssselect(cssselector)[0].text_content().strip()

html = scraperwiki.scrape('http://store-locator.barnesandnoble.com/store/2286')
root = lxml.html.fromstring(html)

for el in root.cssselect('div.eventDisplay'): 
    eventInfo = el.cssselect('span.eventName')[0]
    title = eventInfo.text_content()
    link = eventInfo[0].attrib['href'].strip()
    subtitle = get_text('span.productTitle')
    # Add the subtitle if there is one. 
    title = title + ': ' + subtitle if subtitle else title

    # Get the raw time, removing the comma and splitting it. 
    rtime = get_text('span.eventTime').replace(',', '').split()
    # Format the time and convert it. 
    ftime = '%s %s %s %s' % (rtime[2], rtime[1], rtime[3], rtime[4]+rtime[5])
    time = dateutil.parser.parse(ftime)

    # Category: kids, family, etc.  
    eventType = get_text('span.eventDetails')
    
    id = link.split('/')[-1]
    data = {'id': id, 'title': title, 'link': link, 'type': eventType, 'time': time}
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    