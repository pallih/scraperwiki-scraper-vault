import scraperwiki
import lxml.html 
import datetime

xml = scraperwiki.scrape("http://www.zapiro.com/feed.xml")
root = lxml.html.fromstring(xml)

for item in root.cssselect("item"):
    orig_title = item.cssselect("title")[0].text_content()

    # Where was this originally published?
    last2char = orig_title[-2:]
    if last2char == 'tt':
        where = 'The Times'
    elif last2char == 'st':
        where = 'The Sunday Times'
    elif last2char == 'mg':
        where = 'Mail & Guardian'
    else:
        where = ''

    # New desc
    description = ''

    # Grab the stuff we want from the original desc
    orig_desc = item.cssselect("description")[0].text_content()
    desc = lxml.html.fromstring(orig_desc)

    # Iterate through the <p> in the orig desc and work on each
    i = 0
    for p in desc.cssselect("p"):
        if p.cssselect("img"):
            img = p.cssselect("img")[0].attrib['src']
            description += '<p><img src="http://www.zapiro.com'+img+'" /></p>'

        # A better title is on the 1st line below the img
        if i == 1:
            title = p.text_content().strip() + ' (' + where + ')'

        if i == 3:
            description += lxml.html.tostring(p)
        i += 1
    pubDate = item.cssselect("item pubDate")[0].text_content()
    now = datetime.datetime.now()

    link = item.cssselect("link")[0].text_content()
    data = {
        'link': link,
        'title': title,
        'description': description,
        'pubDate': str(now) ,
    }
    scraperwiki.sqlite.save(unique_keys=['link'],data=data)
