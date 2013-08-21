import scraperwiki,requests,urllib,json,os,cgi
scraperwiki.utils.httpresponseheader("Content-Type", "audio/x-mpegurl") # turn off scraperwiki banner
print "#EXTM3U"
query= os.getenv("QUERY_STRING", "")
print "# Created by ScraperWiki: scraperwiki.com/views/archiveorg_m3u"

# TODO: deal with multiple files [M3U? MP3 ZIP?]
# TODO: make default search not include erroneous modern music

formatlist=[u'Ogg Vorbis', u'160Kbps MP3',u'VBR MP3', u'128Kbps MP3',u'Flac',u'96Kbps MP3',u'64Kbps MP3',u'Windows Media Audio',u'Unknown']
def parsesearch(query="q=date%3A%5B1900-01-01+TO+1909-12-31%5D+AND+mediatype%3Aaudio"):
    baseurl="http://www.archive.org/advancedsearch.php?"
    suffix="&fl%5B%5D=*&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=9999&page=1&output=json&save=yes"
    r=requests.get(baseurl+query+suffix)
    j=json.loads(r.content)
    #print "%d total records found for search" % j['response']['numFound']
    for d in j['response']['docs']:
        found=False
        identifier=d['identifier']
        formats=d['format']
        #print identifier,formats
        for f in formatlist:
            if f in formats:
                try:
                    c=d['creator'][0]
                except:
                    c="Unknown"
                try:
                    t=d['title']
                except:
                    t="Unknown"
                print '#EXTINF:0, %s - %s'%(c,t)
                print 'http://www.archive.org/download/%s/format=%s' % (identifier,urllib.quote_plus(f))
                found=True
                break
        # assert found, "File not found for %s: formats were %s" % (identifier, str(formats)) # sometimes this happens


if query:
    query2=query.replace('query','q')
    parsesearch(query2)
else:
    parsesearch()

