import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dab&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dac&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dad&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dae&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daf&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dag&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dah&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dai&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daj&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dak&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dal&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dam&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dan&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dao&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dap&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daq&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dar&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Das&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dat&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dau&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dav&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daw&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dax&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Day&max=90&links=preserve&exc=&submit=Create+Feed',   
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daz&max=90&links=preserve&exc=&submit=Create+Feed']

for i in range(len(sources)):       


    source = sources[i]

    html = scraperwiki.scrape(source)        #print html
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
    items = soup.findAll('item')             #print type(items) #print items[0]

    article = {}

    for item in items:
        article['title'] = item.find('title').text
        article['url'] = item.find('link').next # wow, this worked!
        article['ingress'] = item.find('description').text
        article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
        article['now'] = datetime.now()
        print article
        # the sensfull thing here would be to build a func to scrape the url form here.

        scraperwiki.sqlite.save(['title'], article)
