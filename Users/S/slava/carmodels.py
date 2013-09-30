import scraperwiki
import lxml.html
import re
# Blank Python

ua="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
html=scraperwiki.scrape("http://www.netcarshow.com/", None, ua)
root=lxml.html.document_fromstring(html)
id=1
for a in root.xpath("/html/body/div[@id='cc']/div[@class='Ll']/div[@class='mFrY']/ul[@class='lst']/li/a"):
    make = a.text_content()
    a.attrib['href']
    html=scraperwiki.scrape("http://www.netcarshow.com"+a.attrib['href'], None, ua)
    root1=lxml.html.document_fromstring(html)
    car=[]
    car.append({'id':id, 'parent_id':0, 'make':make, 'model':'', 'img_url': '', 'type':'make' })
    parent_id=id
    id+=1
    
    for e in root1.xpath("/html/body/div[@id='cc']/div[@class='Ll']/div[@class='lFrX']/ul[@class='lst']/li/a"):
        model = e.text_content()
        imgpart=re.findall(r"\['(.+?)'\]", e.attrib['onmouseover'], re.I|re.U|re.S)

        car.append({'id':id, 'parent_id':parent_id, 'make':make, 'model':model, 'img_url': 'http://img1.netcarshow.com/' + imgpart[0] + '_thumbnail_00.jpg', 'type':'model' })
        id+=1
        

    scraperwiki.sqlite.save(unique_keys=['id'], data=car, table_name="data")import scraperwiki
import lxml.html
import re
# Blank Python

ua="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"
html=scraperwiki.scrape("http://www.netcarshow.com/", None, ua)
root=lxml.html.document_fromstring(html)
id=1
for a in root.xpath("/html/body/div[@id='cc']/div[@class='Ll']/div[@class='mFrY']/ul[@class='lst']/li/a"):
    make = a.text_content()
    a.attrib['href']
    html=scraperwiki.scrape("http://www.netcarshow.com"+a.attrib['href'], None, ua)
    root1=lxml.html.document_fromstring(html)
    car=[]
    car.append({'id':id, 'parent_id':0, 'make':make, 'model':'', 'img_url': '', 'type':'make' })
    parent_id=id
    id+=1
    
    for e in root1.xpath("/html/body/div[@id='cc']/div[@class='Ll']/div[@class='lFrX']/ul[@class='lst']/li/a"):
        model = e.text_content()
        imgpart=re.findall(r"\['(.+?)'\]", e.attrib['onmouseover'], re.I|re.U|re.S)

        car.append({'id':id, 'parent_id':parent_id, 'make':make, 'model':model, 'img_url': 'http://img1.netcarshow.com/' + imgpart[0] + '_thumbnail_00.jpg', 'type':'model' })
        id+=1
        

    scraperwiki.sqlite.save(unique_keys=['id'], data=car, table_name="data")