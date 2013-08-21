#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"

record = {}

def scrapereport(reportlink):
    boldline = 0
    html = scraperwiki.scrape(baseurl+baselink)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#unusefulbottom a")
    #<div id="unusefulbottom">
    for link in links:
        print "LINK GRABBED WITH CSSSELECT", link
        print "link.attrib.get", link.attrib.get('href')
        downloadlink = link.attrib.get('href')
#    print " downloadlink[0].text_content()", downloadlink[0].text_content()
        pdfdata = urllib2.urlopen(baseurl+downloadlink).read()
        print "pdfdata", pdfdata
        xmldata = scraperwiki.pdftoxml(pdfdata)
        print "xmldata", xmldata
        pdfxml = lxml.etree.fromstring(xmldata)
        print "pdfxml", pdfxml
        boldtags = pdfxml.xpath('.//text')
        linenumber = 0
        for heading in boldtags:
            linenumber = linenumber+1
            #print "Heading:", heading.text
            if heading.text is not None:
#                mention = re.match(r'.*NMS.*',heading.text)
                mention = re.match(r'.*overall.*',heading.text)
                if mention:
                    print "FULL LINE", lxml.etree.tostring(heading, encoding="unicode", method="text")
#                    print "OVERALL", heading.text
#                    print "CHECK", pdfxml.xpath('.//text')[linenumber-1].text
#                    print "LINEAFTER", pdfxml.xpath('.//text')[linenumber].text
                    record['overall'] = lxml.etree.tostring(heading, encoding="unicode", method="text")
                    record['uniqueref'] = baselink+"_"+str(boldline)
                    record['downloadlink'] = baseurl+downloadlink
                    scraperwiki.sqlite.save(['uniqueref'],record)

linklist = ['/provider/files/1691253/urn/SC419293.pdf', '/provider/files/1694513/urn/SC038454.pdf', '/provider/files/1800801/urn/SC068071.pdf', '/provider/files/1806005/urn/SC059299.pdf', '/provider/files/1686333/urn/SC035443.pdf', '/provider/files/1683521/urn/SC360644.pdf', '/provider/files/1834445/urn/SC035480.pdf', '/provider/files/1844127/urn/SC039171.pdf', '/provider/files/1812305/urn/SC068751.pdf', '/provider/files/1411447/urn/SC039684.pdf', '/provider/files/1890777/urn/SC039687.pdf', '/provider/files/1405513/urn/SC060540.pdf', '/provider/files/2004653/urn/SC040872.pdf', '/provider/files/1901401/urn/SC035482.pdf', '/provider/files/1912965/urn/SC037800.pdf', '/provider/files/2139499/urn/SC418511.pdf', '/provider/files/2153087/urn/SC396331.pdf', '/provider/files/2070039/urn/SC436472.pdf', '/provider/files/1803701/urn/SC044225.pdf', '/provider/files/2018353/urn/SC403956.pdf', '/provider/files/1924827/urn/SC054728.pdf', '/provider/files/2006541/urn/SC009651.pdf', '/provider/files/1997243/urn/SC042795.pdf', '/provider/files/1910295/urn/SC035477.pdf', '/provider/files/1942003/urn/SC039243.pdf', '/provider/files/1915877/urn/SC402039.pdf', '/provider/files/2019477/urn/SC059945.pdf', '/provider/files/1978331/urn/SC064735.pdf', '/provider/files/2024063/urn/SC034197.pdf', '/provider/files/2024187/urn/SC438244.pdf', '/provider/files/2026791/urn/SC039689.pdf', '/provider/files/2037939/urn/SC066428.pdf', '/provider/files/2041235/urn/SC006013.pdf', '/provider/files/2048947/urn/SC058429.pdf', '/provider/files/2049867/urn/SC402658.pdf', '/provider/files/2050739/urn/SC039087.pdf', '/provider/files/2050995/urn/SC064500.pdf', '/provider/files/2051579/urn/SC062268.pdf', '/provider/files/2051591/urn/SC006017.pdf', '/provider/files/2052251/urn/SC009653.pdf', '/provider/files/2077687/urn/SC411739.pdf', '/provider/files/2077587/urn/SC006010.pdf', '/provider/files/2077551/urn/SC006014.pdf', '/provider/files/2077919/urn/SC039676.pdf', '/provider/files/2078083/urn/SC400219.pdf', '/provider/files/2078051/urn/SC064369.pdf', '/provider/files/2078279/urn/SC416318.pdf', '/provider/files/2077915/urn/SC400880.pdf', '/provider/files/2079247/urn/SC403937.pdf', '/provider/files/2079495/urn/SC411069.pdf', '/provider/files/2079931/urn/SC010087.pdf', '/provider/files/2079675/urn/SC066115.pdf', '/provider/files/1927203/urn/SC368329.pdf', '/provider/files/2080135/urn/SC362165.pdf', '/provider/files/1940387/urn/SC396201.pdf', '/provider/files/2079303/urn/SC403462.pdf', '/provider/files/2015089/urn/SC401603.pdf', '/provider/files/2080631/urn/SC064363.pdf', '/provider/files/2083303/urn/SC039183.pdf', '/provider/files/2082243/urn/SC066245.pdf', '/provider/files/2082595/urn/SC407030.pdf', '/provider/files/2067807/urn/SC035428.pdf', '/provider/files/2069215/urn/SC411046.pdf', '/provider/files/2069163/urn/SC436745.pdf', '/provider/files/2069091/urn/SC064533.pdf', '/provider/files/2069531/urn/SC035439.pdf', '/provider/files/2016753/urn/SC428196.pdf', '/provider/files/2076543/urn/SC010090.pdf', '/provider/files/2076527/urn/SC057700.pdf', '/provider/files/2083675/urn/SC044224.pdf', '/provider/files/2085087/urn/SC039679.pdf', '/provider/files/2085215/urn/SC442401.pdf', '/provider/files/2085871/urn/SC062503.pdf', '/provider/files/2085931/urn/SC052332.pdf', '/provider/files/2086519/urn/SC034944.pdf', '/provider/files/2086567/urn/SC402817.pdf', '/provider/files/2087475/urn/SC039248.pdf', '/provider/files/2089491/urn/SC039673.pdf', '/provider/files/2109807/urn/SC039680.pdf', '/provider/files/2138415/urn/SC035450.pdf', '/provider/files/2140167/urn/SC442402.pdf', '/provider/files/2141175/urn/SC055153.pdf', '/provider/files/2141107/urn/SC440309.pdf', '/provider/files/2141795/urn/SC006019.pdf', '/provider/files/2141787/urn/SC359836.pdf', '/provider/files/2144767/urn/SC039683.pdf', '/provider/files/2145407/urn/SC441717.pdf', '/provider/files/2145375/urn/SC412979.pdf', '/provider/files/2145927/urn/SC050766.pdf', '/provider/files/2146023/urn/SC406893.pdf', '/provider/files/2148235/urn/SC060750.pdf', '/provider/files/2149663/urn/SC044231.pdf', '/provider/files/2149975/urn/SC067870.pdf', '/provider/files/2151351/urn/SC053145.pdf', '/provider/files/2151367/urn/SC375824.pdf', '/provider/files/2151355/urn/SC063959.pdf', '/provider/files/2151387/urn/SC362135.pdf', '/provider/files/2153947/urn/SC412971.pdf', '/provider/files/2154503/urn/SC432741.pdf', '/provider/files/2154527/urn/SC361129.pdf', '/provider/files/2154959/urn/SC061803.pdf', '/provider/files/2155647/urn/SC009648.pdf', '/provider/files/2156115/urn/SC424978.pdf', '/provider/files/2157199/urn/SC421197.pdf', '/provider/files/2157291/urn/SC039134.pdf', '/provider/files/2160027/urn/SC410102.pdf', '/provider/files/2162603/urn/SC067053.pdf', '/provider/files/2163611/urn/SC063759.pdf', '/provider/files/2164215/urn/SC063103.pdf', '/provider/files/2164279/urn/SC035454.pdf', '/provider/files/2164731/urn/SC035459.pdf', '/provider/files/2166251/urn/SC390201.pdf', '/provider/files/2167979/urn/SC006011.pdf', '/provider/files/2170495/urn/SC009651.pdf']

for baselink in linklist:
    print "scraping:",'http://www.ofsted.gov.uk'+baselink
    scrapereport('http://www.ofsted.gov.uk'+baselink)

#this thread on stackoverflow used to grab <b> tags inside ratings line: 
#http://stackoverflow.com/questions/4770191/lxml-etree-element-text-doesnt-return-the-entire-text-from-an-element

#for this error: 'ascii' codec can't encode character u'\u2019' in position 70: ordinal not in range(128)
#added encoding="unicode", to two lines