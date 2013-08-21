"""
The view of HaodooScraper.

Parameters:
 * q : keyword, need to encode as utf-8.

Output:
 JSON dictionary.

Example:
 q=%e9%be%8d
"""
import scraperwiki
import cgi, os
import simplejson as json

def unicode_to_ascii(us):
    """
    The data in unicode string actually is utf-8, so we need to convert it to ascii string.
    Then convert it via decode.
    """
    return "".join([chr(ord(c)) for c in us])

paramdict=dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
where_sql=""
if paramdict.has_key('q'):
    uq=unicode_to_ascii(paramdict['q']).decode('utf-8')
    # print( "// {0}".format( repr(uq)[1:] ) )
    uqs=uq.split(u' ')
    uqs_len=len(uqs)
    # print(uqs_len)
    if uqs_len==2:
        # author, keyword
        where_sql=u" where (title like '%{0}%' or title like '%{1}%') and (author like '%{0}%' or author like '%{1}%')".format(uqs[0], uqs[1])
    elif uqs_len==1:
        # not sure
        where_sql = u" where title like '%{0}%' or author like '%{0}%'".format( uqs[0] )
    # print( where_sql )

sourcescraper = 'haodooscraper'
scraperwiki.sqlite.attach( sourcescraper )
volumes = scraperwiki.sqlite.select( "* from HaodooScraper.bookvolumes " + where_sql + " limit 10")
for volume in volumes:
    volume['type'] = scraperwiki.sqlite.select( "type, link from HaodooScraper.volumeexts where volumeid='{0}'".format( volume['id'] ) )
    book = scraperwiki.sqlite.select( "url from HaodooScraper.bookpages where id='{0}'".format( volume['bookid'] ) )
    volume['url'] = book[0]['url']

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")

print( json.dumps( volumes ) )


