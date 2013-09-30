import scraperwiki
import lxml.html

r = range(10)

for page in r:

  html = scraperwiki.scrape("http://www.ascodevida.com/mejores/todos/p/"+str(page+1))

  content = lxml.html.fromstring(html)

  elements = content.cssselect('p.story_content a')

  for element in elements:
    link = element.get('href')
    token = link.replace('http://www.ascodevida.com/','')
    arr = token.split('/')
    cat = arr[0]
    id = arr[1]
    data = {
      'id': id,
      'position': page*10 + elements.index(element) + 1,
      'cat': cat,
      'token': token,
      'description': element.text_content(),
      'link': link
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import lxml.html

r = range(10)

for page in r:

  html = scraperwiki.scrape("http://www.ascodevida.com/mejores/todos/p/"+str(page+1))

  content = lxml.html.fromstring(html)

  elements = content.cssselect('p.story_content a')

  for element in elements:
    link = element.get('href')
    token = link.replace('http://www.ascodevida.com/','')
    arr = token.split('/')
    cat = arr[0]
    id = arr[1]
    data = {
      'id': id,
      'position': page*10 + elements.index(element) + 1,
      'cat': cat,
      'token': token,
      'description': element.text_content(),
      'link': link
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
