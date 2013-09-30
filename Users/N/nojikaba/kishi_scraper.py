import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.shogi.or.jp/player/kishi/watanabe-a.html")
root = lxml.html.fromstring(html)

name = root.cssselect("div.cont h3")[0]

number = root.cssselect("div.maintxt dl dd")[0]
birth_r = root.cssselect("div.maintxt dl dd")[1]
ryuo = root.cssselect("div.maintxt dl dd")[4]
juni = root.cssselect("div.maintxt dl dd")[5]

birth = re.sub(r'月|年|日','/',birth_r.text)

print birth
data = {
    'name':name.text,
    'number':number.text,
    'birth':birth,
    'ryuo':ryuo.text,
    'juni':juni.text
}
scraperwiki.sqlite.save(unique_keys=['name'],data=data)

import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.shogi.or.jp/player/kishi/watanabe-a.html")
root = lxml.html.fromstring(html)

name = root.cssselect("div.cont h3")[0]

number = root.cssselect("div.maintxt dl dd")[0]
birth_r = root.cssselect("div.maintxt dl dd")[1]
ryuo = root.cssselect("div.maintxt dl dd")[4]
juni = root.cssselect("div.maintxt dl dd")[5]

birth = re.sub(r'月|年|日','/',birth_r.text)

print birth
data = {
    'name':name.text,
    'number':number.text,
    'birth':birth,
    'ryuo':ryuo.text,
    'juni':juni.text
}
scraperwiki.sqlite.save(unique_keys=['name'],data=data)

