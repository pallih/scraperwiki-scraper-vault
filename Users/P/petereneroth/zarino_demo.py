import scraperwiki
import requests
import lxml.html

# Blank Python

peter = "hej"
print peter

def scrape_people():
  for i in range(1,15):
        print 'scraping page %s' % i
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
        dom = lxml.html.fromstring(r)
        for student in dom.cssselect('div.community_list td'):
            d = {
                'name': student.cssselect('h6')[0].text,
                'url': student.cssselect('a')[0].get('href'),
                'course': student.cssselect('p.subtitle')[0].text,
                #'avatar': student.cssselect('img')[0].get('src')
            }
            scraperwiki.sqlite.save(['url'], d)

scrape_people()

#for i in range(1,20):
    #http://www.hyperisland.com/people?filter=true&page=1&role=student

