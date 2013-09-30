import urllib
import urlparse
import scraperwiki

#1.    Store the URL http://www.youtube.com/watch?v=q25jkSHIT7I&feature=feedf as a string in a variable.
url = "http://www.youtube.com/watch?v=q25jkSHIT7I&feature=feedf"

#2.    Parse it into its component parts and print out the parsed object.
parsed = urlparse.urlparse(url)
print parsed
urlscheme = parsed.scheme
print urlscheme
urlnetloc = parsed.netloc
print urlnetloc
urlpath = parsed.path
print urlpath


#3.    Extract the query string from the URL and print that
urlquery = parsed.query
print urlquery, type(urlquery)

#4.    Extract the video hash code from the query string.
queriedstring = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
print queriedstring

#5.    Reconstruct the original URL from the decomposed parts.
print urlparse.urlunparse(parsed)

#6.    Alter the decomposed parts, to change the value of v= to “catcatcatcatcat”, and then reconstruct a new URL.
d = urlparse.parse_qs(urlparse.urlparse(url).query)
d['v'][0]= 'catcatcatcatcat'

querystring = urllib.urlencode(d,True)

print urlparse.urlunparse( (urlscheme, urlnetloc,urlpath,'', querystring ,'',) )

#7.    Take the URL http://www.guardian.co.uk/politics, and with a URL join function alter it to change the path to “/environment”.
print urlparse.urljoin( 'http://www.guardian.co.uk/politics', '/environment')

#8.    Take the URL http://www.guardian.co.uk/politics/conservatives, Get the contents of the page at that URL and print out the HTML.
htmlcon = scraperwiki.scrape('http://www.guardian.co.uk/politics/conservatives')
print htmlcon

#9.    With a URL join function alter it with the relative path “../labour” to create a new URL. Get the contents of that page.
htmllab = scraperwiki.scrape(urlparse.urljoin ('http://www.guardian.co.uk/politics/conservatives', '../labour'))
print htmllab

#10.    Find a form which needs a POST request and using urllib call it and get the HTML back.
urlpost = 'http://www.tesco.com/storelocator/'
data = {}
data['value'] = 'W60TR'
param = urllib.urlencode(data)
htmlpost = urllib.urlopen(urlpost, param).read()
print htmlpost
import urllib
import urlparse
import scraperwiki

#1.    Store the URL http://www.youtube.com/watch?v=q25jkSHIT7I&feature=feedf as a string in a variable.
url = "http://www.youtube.com/watch?v=q25jkSHIT7I&feature=feedf"

#2.    Parse it into its component parts and print out the parsed object.
parsed = urlparse.urlparse(url)
print parsed
urlscheme = parsed.scheme
print urlscheme
urlnetloc = parsed.netloc
print urlnetloc
urlpath = parsed.path
print urlpath


#3.    Extract the query string from the URL and print that
urlquery = parsed.query
print urlquery, type(urlquery)

#4.    Extract the video hash code from the query string.
queriedstring = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
print queriedstring

#5.    Reconstruct the original URL from the decomposed parts.
print urlparse.urlunparse(parsed)

#6.    Alter the decomposed parts, to change the value of v= to “catcatcatcatcat”, and then reconstruct a new URL.
d = urlparse.parse_qs(urlparse.urlparse(url).query)
d['v'][0]= 'catcatcatcatcat'

querystring = urllib.urlencode(d,True)

print urlparse.urlunparse( (urlscheme, urlnetloc,urlpath,'', querystring ,'',) )

#7.    Take the URL http://www.guardian.co.uk/politics, and with a URL join function alter it to change the path to “/environment”.
print urlparse.urljoin( 'http://www.guardian.co.uk/politics', '/environment')

#8.    Take the URL http://www.guardian.co.uk/politics/conservatives, Get the contents of the page at that URL and print out the HTML.
htmlcon = scraperwiki.scrape('http://www.guardian.co.uk/politics/conservatives')
print htmlcon

#9.    With a URL join function alter it with the relative path “../labour” to create a new URL. Get the contents of that page.
htmllab = scraperwiki.scrape(urlparse.urljoin ('http://www.guardian.co.uk/politics/conservatives', '../labour'))
print htmllab

#10.    Find a form which needs a POST request and using urllib call it and get the HTML back.
urlpost = 'http://www.tesco.com/storelocator/'
data = {}
data['value'] = 'W60TR'
param = urllib.urlencode(data)
htmlpost = urllib.urlopen(urlpost, param).read()
print htmlpost
