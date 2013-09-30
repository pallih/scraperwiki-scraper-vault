"Which panels are you most excited about?"
from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select, execute

DOMAIN = "http://cindyroyal.net"
BOARD = "http://cindyroyal.net/advanced/?q=forums/sxsw-overview"

def scrape():
    d = getTopics(BOARD)
    save(['topic-href'], d, 'topics')
    topic_hrefs = [row['topic-href'] for row in d]
    for topic_href in topic_hrefs:
        d = parseTopic(topic_href)
        save([], d, 'links')

def getTopics(url):
    x = fromstring(urlopen(url).read())
    topics = x.xpath('id("forum-topic-9")/descendant::td[descendant::a]')
    d = [{
        "title": topic.cssselect('a')[0].text,
        "topic-href": topic.cssselect('a')[0].attrib['href'],
        "author": topic.cssselect('.username')[0].text
    } for topic in topics]
    return d

def parseTopic(topichref):
    x = fromstring(urlopen(DOMAIN + topichref).read())
    bodylinks = x.cssselect('div.field-items a')
    d = [{"topic-href": topichref, "link-href": link.attrib['href'], "link-title": link.text} for link in bodylinks]
    return d

def analyze():
    d = select("""
  `link-href`, GROUP_CONCAT(`author`) AS `authors`, count(*) AS "count"
FROM `links`
JOIN `topics` ON `links`.`topic-href` = `topics`.`topic-href`
GROUP BY `link-href`
""")
    execute('DROP TABLE IF EXISTS `wrote-about-same-things`')
    save([], d, 'wrote-about-same-things')
    print '''
These look most exciting because three different people wrote about each.

3    Kiana Fitzgerald,Sara Peralta,Susan Raybuck    http://schedule.sxsw.com/2012/events/event_IAP100409
3    Shawn Dullye,Joe Vasquez,Sara Peralta          http://schedule.sxsw.com/2012/events/event_IAP10593
3    Shawn Dullye,Kiana Fitzgerald,Sara Peralta     http://schedule.sxsw.com/2012/events/event_IAP13848

Of course, that isn't adjusted for how many each person wrote.
'''

    d = select("""
  author, count(*) AS `how-many` FROM `links`
JOIN topics on links.`topic-href` = topics.`topic-href`
GROUP BY author
ORDER BY 2 DESC
""")
    save(['author'], d, 'how-many-did-you-link')
    print """
And Sara's really excited
http://cindyroyal.net/advanced/?q=content/wanted-time-travel-technology-0
"""

#scrape()
analyze()"Which panels are you most excited about?"
from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select, execute

DOMAIN = "http://cindyroyal.net"
BOARD = "http://cindyroyal.net/advanced/?q=forums/sxsw-overview"

def scrape():
    d = getTopics(BOARD)
    save(['topic-href'], d, 'topics')
    topic_hrefs = [row['topic-href'] for row in d]
    for topic_href in topic_hrefs:
        d = parseTopic(topic_href)
        save([], d, 'links')

def getTopics(url):
    x = fromstring(urlopen(url).read())
    topics = x.xpath('id("forum-topic-9")/descendant::td[descendant::a]')
    d = [{
        "title": topic.cssselect('a')[0].text,
        "topic-href": topic.cssselect('a')[0].attrib['href'],
        "author": topic.cssselect('.username')[0].text
    } for topic in topics]
    return d

def parseTopic(topichref):
    x = fromstring(urlopen(DOMAIN + topichref).read())
    bodylinks = x.cssselect('div.field-items a')
    d = [{"topic-href": topichref, "link-href": link.attrib['href'], "link-title": link.text} for link in bodylinks]
    return d

def analyze():
    d = select("""
  `link-href`, GROUP_CONCAT(`author`) AS `authors`, count(*) AS "count"
FROM `links`
JOIN `topics` ON `links`.`topic-href` = `topics`.`topic-href`
GROUP BY `link-href`
""")
    execute('DROP TABLE IF EXISTS `wrote-about-same-things`')
    save([], d, 'wrote-about-same-things')
    print '''
These look most exciting because three different people wrote about each.

3    Kiana Fitzgerald,Sara Peralta,Susan Raybuck    http://schedule.sxsw.com/2012/events/event_IAP100409
3    Shawn Dullye,Joe Vasquez,Sara Peralta          http://schedule.sxsw.com/2012/events/event_IAP10593
3    Shawn Dullye,Kiana Fitzgerald,Sara Peralta     http://schedule.sxsw.com/2012/events/event_IAP13848

Of course, that isn't adjusted for how many each person wrote.
'''

    d = select("""
  author, count(*) AS `how-many` FROM `links`
JOIN topics on links.`topic-href` = topics.`topic-href`
GROUP BY author
ORDER BY 2 DESC
""")
    save(['author'], d, 'how-many-did-you-link')
    print """
And Sara's really excited
http://cindyroyal.net/advanced/?q=content/wanted-time-travel-technology-0
"""

#scrape()
analyze()