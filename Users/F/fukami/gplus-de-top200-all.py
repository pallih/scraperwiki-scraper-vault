import scraperwiki
import lxml.html

def parse_page(id):
    html = scraperwiki.scrape("http://gpluscharts.de/detail.php?id="+str(id))
    root = lxml.html.fromstring(html)
    follow = root.cssselect('div.userinfo div.rightcol div.row span.right')
    name = root.cssselect('a.userinfo')
    gid = name[0].attrib.get('href').replace('http://noreferer.de/?https://plus.google.com','').replace('/','')
    following = follow[0].text_content()
    if following == '-':
        following = 0
    if name[0].text_content() != '':
        data = {
            'GID'        : int(gid),
            'Name'       : name[0].text_content(),
            'Following'  : int(following),
            'Followers'  : int(follow[1].text_content()),
        }
        print id, data
        scraperwiki.sqlite.save(unique_keys=['GID'], data=data, table_name="gplusdetop200all")

#for i in range(23,35):
for i in range(1,1320):
    try:
        parse_page(i)
    except:
        print i, "No data"import scraperwiki
import lxml.html

def parse_page(id):
    html = scraperwiki.scrape("http://gpluscharts.de/detail.php?id="+str(id))
    root = lxml.html.fromstring(html)
    follow = root.cssselect('div.userinfo div.rightcol div.row span.right')
    name = root.cssselect('a.userinfo')
    gid = name[0].attrib.get('href').replace('http://noreferer.de/?https://plus.google.com','').replace('/','')
    following = follow[0].text_content()
    if following == '-':
        following = 0
    if name[0].text_content() != '':
        data = {
            'GID'        : int(gid),
            'Name'       : name[0].text_content(),
            'Following'  : int(following),
            'Followers'  : int(follow[1].text_content()),
        }
        print id, data
        scraperwiki.sqlite.save(unique_keys=['GID'], data=data, table_name="gplusdetop200all")

#for i in range(23,35):
for i in range(1,1320):
    try:
        parse_page(i)
    except:
        print i, "No data"