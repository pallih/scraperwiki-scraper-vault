import scraperwiki

# Blank Python

print "Hello, Winnipeg crime!"
import scraperwiki
html = scraperwiki.scrape("http://www.winnipeg.ca/police/press/2012/01jan/2012_01_31.stm")
print html
import lxml.html
root = lxml.html.fromstring(html)
from lxml.html import builder as E
from lxml.html import usedoctest
html = E.HTML(
E.HEAD(
E.LINK(rel="stylesheet", href="great.css", type="text/css"),
E.TITLE("Best Page Ever")
E.BODY(
E.H1(E.CLASS("heading"), "Top News"),
E.P("World News only on this page", style="font-size: 200%"),
"Ah, and here's some more text, by the way.",
lxml.html.fromstring("<p>... and this is a parsed fragment ...</p>")
..)
..)
>>> print lxml.html.tostring(html)
<html>
  <head>
    <link href="great.css" rel="stylesheet" type="text/css">
    <title>Best Page Ever</title>
  </head>
  <body>
    <h1 class="heading">Top News</h1>
    <p style="font-size: 200%">World News only on this page</p>
    Ah, and here's some more text, by the way.
    <p>... and this is a parsed fragment ...</p>
  </body>
</html>


