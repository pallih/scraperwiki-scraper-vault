import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=content&rvexpandtemplate").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=content&rvexpandtemplate"

#Parse the url as xml

article = lxml.etree.parse(urllib.urlopen(url))

#Use XPath to select the element we want to look at

revs = article.xpath('//rev')import scraperwiki
import lxml.etree
import urllib

#Print out the content returned by the API; helps with debuggung
url = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=content&rvexpandtemplate").read()

print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=content&rvexpandtemplate"

#Parse the url as xml

article = lxml.etree.parse(urllib.urlopen(url))

#Use XPath to select the element we want to look at

revs = article.xpath('//rev')