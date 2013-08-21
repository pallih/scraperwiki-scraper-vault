def shorten_target(target_url):
    """
    Error checking left as an exercise
    """
    import urllib2, json

    shorten_svc = 'https://www.googleapis.com/urlshortener/v1/url'
    data = '{"longUrl": "%s"}' % target_url
    request = urllib2.Request(shorten_svc,  data, 
                              {'Content-Type': 'application/json'})
    response = json.loads( urllib2.urlopen(request).read() )
    return response[u'id']

print shorten_target('http://scraperwiki.com')


