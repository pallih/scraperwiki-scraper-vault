import scraperwiki

cfg_link = "http://rnz.hrt.hr/"
cfg_emisija_filter = scraperwiki.utils.GET()["emisija"]

scraperwiki.sqlite.attach("hrt_rnz")

scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

print """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>HRT Radio na zahtjev</title>
<description>Hrvatski radio - Radio na zahtjev</description>
<link>{0}</link>
<image>
<url>http://www.hrt.hr/fileadmin/logo.png</url>
<title>Hrvatski radio</title>
</image>
""".format(cfg_link)

data = scraperwiki.sqlite.select(
    '''* from 'swdata' where emisija='{0}' order by datum desc'''.format(cfg_emisija_filter)
)

for d in data:
    print "<item>"
    print u"<title>{0}: {1}</title>".format(d["emisija"], d["naslov"])
    print u"<description>{0}: {1}, \n veli\u010Dina: {2}, \n trajanje: {3}</description>".format(d["emisija"], d["naslov"], d["velicina"], d["trajanje"])
    print "<link>{0}</link>".format(cfg_link)
    print "<guid>{0}{1}</guid>".format(cfg_link, d["link"])
    print "<enclosure url='{0}{1}' length='{2}' type='audio/mpeg'/>".format(cfg_link, d["link"], d["velicina"])
    print "<pubDate>", d["datum"], "</pubDate>"
    print "<category>podcasts</category>"
    print "</item>"

print """</channel>
</rss>"""


import scraperwiki

cfg_link = "http://rnz.hrt.hr/"
cfg_emisija_filter = scraperwiki.utils.GET()["emisija"]

scraperwiki.sqlite.attach("hrt_rnz")

scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

print """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>HRT Radio na zahtjev</title>
<description>Hrvatski radio - Radio na zahtjev</description>
<link>{0}</link>
<image>
<url>http://www.hrt.hr/fileadmin/logo.png</url>
<title>Hrvatski radio</title>
</image>
""".format(cfg_link)

data = scraperwiki.sqlite.select(
    '''* from 'swdata' where emisija='{0}' order by datum desc'''.format(cfg_emisija_filter)
)

for d in data:
    print "<item>"
    print u"<title>{0}: {1}</title>".format(d["emisija"], d["naslov"])
    print u"<description>{0}: {1}, \n veli\u010Dina: {2}, \n trajanje: {3}</description>".format(d["emisija"], d["naslov"], d["velicina"], d["trajanje"])
    print "<link>{0}</link>".format(cfg_link)
    print "<guid>{0}{1}</guid>".format(cfg_link, d["link"])
    print "<enclosure url='{0}{1}' length='{2}' type='audio/mpeg'/>".format(cfg_link, d["link"], d["velicina"])
    print "<pubDate>", d["datum"], "</pubDate>"
    print "<category>podcasts</category>"
    print "</item>"

print """</channel>
</rss>"""


