import scraperwiki
import requests
import lxml.html
# Blank Python

for page in range(1,115):
    print page
    url='http://textface.com/posts?page=%d'%page
    html=requests.get(url).content
    root=lxml.html.fromstring(html)
    for article in root.xpath("//article[@class='post_in_stream']"):
        data={}
        data['title']=article.cssselect('h2')[0].text_content()
        data['url']=article.cssselect('h2 a')[0].attrib['href']
        data['good']=article.cssselect("span[class='good_ratings']")[0].text_content()
        data['bad']=article.cssselect("span[class='bad_ratings']")[0].text_content()
        data['img']=article.cssselect("div[class='the_content'] img")[0].attrib['src']
        data['caption']=article.cssselect("h6[class='subheading']")[0].text_content()
        scraperwiki.sqlite.save(table_name='textface', data=data, unique_keys=['url'])

