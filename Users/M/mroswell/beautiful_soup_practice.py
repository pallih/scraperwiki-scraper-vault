import scraperwiki
from bs4 import BeautifulSoup

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
oup = BeautifulSoup(open("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS"))

html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


soup = BeautifulSoup(html_doc)

print(soup.prettify())

print soup.title
# <title>The Dormouse's story</title>

print soup.title.name
# u'title'

print soup.title.string
# u'The Dormouse's story'

print soup.title.parent.name
# u'head'

print soup.p
# <p class="title"><b>The Dormouse's story</b></p>

print soup.p['class']
# u'title'

print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

print soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

for link in soup.find_all('a'):
    print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie


import scraperwiki
from bs4 import BeautifulSoup

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
oup = BeautifulSoup(open("http://mgaleg.maryland.gov/webmga/frmMain.aspx?pid=legisrpage&tab=subject6&ys=2013RS"))

html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


soup = BeautifulSoup(html_doc)

print(soup.prettify())

print soup.title
# <title>The Dormouse's story</title>

print soup.title.name
# u'title'

print soup.title.string
# u'The Dormouse's story'

print soup.title.parent.name
# u'head'

print soup.p
# <p class="title"><b>The Dormouse's story</b></p>

print soup.p['class']
# u'title'

print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

print soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

for link in soup.find_all('a'):
    print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie


