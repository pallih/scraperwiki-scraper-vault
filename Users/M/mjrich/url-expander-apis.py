import sys, httplib2, urllib
import xml.etree.ElementTree as ET



#Be nice to these APIs.  If you're planning to make many calls, pass User-Agent headings and probably best to get in touch with groups directly.


def url_enlarger(url): #function to call URL expander service. (https://code.google.com/p/url-enlarger/)
    h = httplib2.Http(".cache")
    response, content = h.request("http://url-enlarger.appspot.com/api?url="+url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return content

def long_url(url): #function to call Long URL service. (http://longurl.org/)
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request("http://api.longurl.org/v2/expand?url="+urllib.quote(url), "GET")
    root= ET.fromstring(content)
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return root[0].text


#Examples
print url_enlarger('http://bit.ly/NN0k0Z')
print long_url('http://bit.ly/NN0k0Z')


import sys, httplib2, urllib
import xml.etree.ElementTree as ET



#Be nice to these APIs.  If you're planning to make many calls, pass User-Agent headings and probably best to get in touch with groups directly.


def url_enlarger(url): #function to call URL expander service. (https://code.google.com/p/url-enlarger/)
    h = httplib2.Http(".cache")
    response, content = h.request("http://url-enlarger.appspot.com/api?url="+url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return content

def long_url(url): #function to call Long URL service. (http://longurl.org/)
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request("http://api.longurl.org/v2/expand?url="+urllib.quote(url), "GET")
    root= ET.fromstring(content)
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return root[0].text


#Examples
print url_enlarger('http://bit.ly/NN0k0Z')
print long_url('http://bit.ly/NN0k0Z')


