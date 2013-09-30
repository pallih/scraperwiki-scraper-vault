import scraperwiki

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import lxml.html

#url = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=1"

#br = mechanize.Browser()
#response = br.open(url)


#for pagenum in range(3):
#    html = response.read()
#    print "Page %d  page length %d" % (pagenum, len(html))
#    print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

for i in range(78):
    html = scraperwiki.scrape("http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=" + str(i))
    root = lxml.html.fromstring(html)
    for tr in root.cssselect('.grid-item'):
        data = {}
        img = tr.cssselect(".img-wrapper img")
        data['img'] = img[0].get('src')
        cr = tr.cssselect('.content-region h3 a')
        data['name'] = cr[0].text_content()
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)import scraperwiki

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import lxml.html

#url = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=1"

#br = mechanize.Browser()
#response = br.open(url)


#for pagenum in range(3):
#    html = response.read()
#    print "Page %d  page length %d" % (pagenum, len(html))
#    print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

for i in range(78):
    html = scraperwiki.scrape("http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=" + str(i))
    root = lxml.html.fromstring(html)
    for tr in root.cssselect('.grid-item'):
        data = {}
        img = tr.cssselect(".img-wrapper img")
        data['img'] = img[0].get('src')
        cr = tr.cssselect('.content-region h3 a')
        data['name'] = cr[0].text_content()
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)