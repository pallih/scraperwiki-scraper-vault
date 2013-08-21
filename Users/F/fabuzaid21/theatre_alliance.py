import scraperwiki
from BeautifulSoup import BeautifulSoup

def strip_tags(html):
    return ' '.join(html.findAll(text=True))

starting_url = 'http://www.theatrealliance.org/event-calendar/feed'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

items = soup.findAll('item')
#print type(items)
#print items[0]

record = {}
 
for item in items:
    titleTag = item.find('title')
    title = titleTag.text
    record['title'] = title
    descriptionTag = item.find('description')
    #print descriptionTag
    # This description tag has a bunch of well-structured data in it, so let's take a second to dig it out.
    # Venue
    dt = BeautifulSoup(descriptionTag.contents[0])
    venue = dt.find('div', 'field-field-venue').p
    if venue is not None:
        venue = strip_tags(venue)
    record['venue'] = venue
    #print venue

    # Start date
    sdate = dt.find('div','field-field-open-date').find('span','date-display-start')
    if sdate:
        sdate = sdate.string
    else:
        sdate = dt.find('div','field-field-open-date').find('span','date-display-single').string
    record['startDate'] = sdate
    #print sdate
    
    # End date
    fdate = dt.find('div','field-field-open-date').find('span','date-display-end')
    if fdate:
        fdate = fdate.string
    else:
        fdate = None
    record['endDate'] = fdate
    #print fdate

    # Individual event dates
    eventDates = dt.find('div','field-field-event-date').findAll('span','date-display-single')
    evArr = []
    for ev in eventDates:
        if ev.string is not None:
            evArr.append(ev.string)

    if len(evArr) > 0:
        evDates = "|".join(evArr)
    else:
        evDates = None
    record['eventDates'] = evDates
    #print evDates

    # Price range
    priceRange = dt.find('div','field-field-price-range')
    if priceRange:
        priceRange = priceRange.find('div','field-item').string
    else:
        priceRange = None
    record['priceRange'] = priceRange
    #print priceRange

    # Description
    description = dt.find('div','field-field-additional-crew')
    if description is not None:
        description = description.findPreviousSibling('p')

    record['description'] = description
    #print description

    # Additional info
    additionalInfo = dt.find('div','field-field-additional-crew')
    if additionalInfo:
        additionalInfo = strip_tags(additionalInfo.find('div','field-item').p)
    else:
        additionalInfo = None
    record['additionalInfo'] = additionalInfo
    #print additionalInfo
    #print descriptionTag
    #print record
    
    scraperwiki.sqlite.save(['title'], record)


