import scraperwiki
import lxml.html

#START

tstart = 1
tcount = 1
while (tstart < 5):
    html = scraperwiki.scrape('http://kat.ph/movies/%d/' % tstart)
    root = lxml.html.fromstring(html)

    for trow in root.cssselect('tr.firstr ~ tr'):
        tname = trow.cssselect('div.torrentname a')[1].text_content()
        tsize = trow.cssselect('td')[1].text_content()
        tfiles = trow.cssselect('td')[2].text_content()
        tage = trow.cssselect('td')[3].text_content()
        tseed = trow.cssselect('td')[4].text_content()
        tleech = trow.cssselect('td')[5].text_content()
        
        torrent  = {
            'name' : tname,
            'size' : tsize,
            'files' : tfiles,
            'age' : tage,
            'seed' : tseed,
            'leech' : tleech
        }
        print scraperwiki.sqlite.save(unique_keys=['id'], data=torrent)
        tcount += 1
        #break


    tstart += 1
    print tstart
    #break
import scraperwiki
import lxml.html

#START

tstart = 1
tcount = 1
while (tstart < 5):
    html = scraperwiki.scrape('http://kat.ph/movies/%d/' % tstart)
    root = lxml.html.fromstring(html)

    for trow in root.cssselect('tr.firstr ~ tr'):
        tname = trow.cssselect('div.torrentname a')[1].text_content()
        tsize = trow.cssselect('td')[1].text_content()
        tfiles = trow.cssselect('td')[2].text_content()
        tage = trow.cssselect('td')[3].text_content()
        tseed = trow.cssselect('td')[4].text_content()
        tleech = trow.cssselect('td')[5].text_content()
        
        torrent  = {
            'name' : tname,
            'size' : tsize,
            'files' : tfiles,
            'age' : tage,
            'seed' : tseed,
            'leech' : tleech
        }
        print scraperwiki.sqlite.save(unique_keys=['id'], data=torrent)
        tcount += 1
        #break


    tstart += 1
    print tstart
    #break
