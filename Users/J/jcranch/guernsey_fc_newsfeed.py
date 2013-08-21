import scraperwiki
import cgi
import os

sourcescraper = 'guernsey_fc_news'
scraperwiki.sqlite.attach(sourcescraper)
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")



def news():
    return scraperwiki.sqlite.select("* from swdata")


def getargs():
    arguments = {}
    for (k,v) in cgi.parse_qsl(os.getenv("QUERY_STRING", "")):
        if k not in arguments:
            arguments[k] = []
        arguments[k].append(v)
    return arguments


def rss():
    print '<?xml version="1.0"?>'
    print '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">'
    print '  <channel>'
    print '    <title>Guernsey FC News</title>'
    print '    <link>http://www.guernseyfc.com/news</link>'
    print '    <description>News articles about Guernsey Football Club</description>'
    print '    <language>en-gb</language>'
    print '    <copyright>2012 Guernsey Football Club LBG | Registered Company Number 53182 | Registered Guernsey Charity Number CH382</copyright>'
    print '    <docs>http://www.rssboard.org/rss-specification</docs>'
    print '    <atom:link href="https://views.scraperwiki.com/run/guernsey_fc_newsfeed/" rel="self" type="application/rss+xml" />'

    for d in news():
        print '    <item>'
        print '      <title>%s</title>'%d["title"]
        print '      <link>%s</link>'%(d["url"].replace("&","&amp;"))
        print '      <description>%s</description>'%d["head"]
        print '      <guid isPermaLink="true">%s</guid>'%(d["url"].replace("&","&amp;"))
        print '    </item>'

    print '  </channel>'
    print '</rss>'


def main():
    args = getargs()
    if u"format" not in args:
        rss()
    elif u"format" == u"rss2.0":
        rss()
    

main()
