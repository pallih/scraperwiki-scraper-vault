import scraperwiki
import lxml.html
from collections import OrderedDict

html = scraperwiki.scrape('https://developer.apple.com/wwdc/videos/index.php')
root = lxml.html.fromstring(html)
for li in root.cssselect('li.session'):
    title = li.cssselect('li.title')[0].text
    track = li.cssselect('li.track')[0].text
    id = li.cssselect('li.id')[0].text
    tmp = set(a.text for a in li.cssselect('a'))
    hd = 'HD' in tmp
    sd = 'SD' in tmp
    pdf = 'PDF' in tmp
    data = OrderedDict([('id', id), ('track', track), ('title', title), ('hd', hd), ('sd', sd), ('pdf', pdf)])
    data = dict(data)
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
