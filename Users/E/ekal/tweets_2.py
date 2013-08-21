# Blank Python
import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://twapperkeeper.com/hashtag/ge10?s5=&s3=&sy=&shh=&smm=&em=5&ed=6&ey=2010&ehh=&emm=&o=&l=10000&from_user=&text=&lang=")
root = lxml.html.fromstring(html)
for div in root.cssselect("div[style='float:left; width:600px']"):
    t = div.cssselect("i")
    data = {
        'tweet' : div.text_content().replace(t[0].text_content() + 'tweet details', ' '),
        'date'  : t[0].text_content()
    }
    if "#ge2010" not in data['tweet'].lower() and "#ukelection" not in data['tweet'].lower() and "#election2010" not in data['tweet'].lower():    
        print data 
        scraperwiki.sqlite.save(unique_keys=['tweet'], data=data)

