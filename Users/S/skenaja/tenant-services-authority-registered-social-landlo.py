import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

# data is from:  https://rsr.tenantservicesauthority.org/RSRDocuments
# GET parameters for each page:  ?year=2010&page=n (1 to 57)
# each page contains a number of repeating UL elements:

#<li>
#
#              <ul class="RSRDataLink">
#
#                   <li class="RSRDataNumber"><a target="_blank" href="/RSRDocuments/Download?path=RSLReports%5C2010%5CSL3344.pdf&DocumentId=-2147483648&RSLNumber=SL3344"><em>SL3344</em></a></li>
#
#                   <li class="RSRDataName">'Johnnie' Johnson Housing Association Limited</li>
#
#                   
#
#                   <li class="RSRDataView"><a href="/RSRDocuments/ShowShortSummary?year=2010&code=SL3344">Summary Report</a></li>
#
#                   
#
#               </ul>
#
#           </li>

# From this need to scrape:  RSL Name (from RSRDataName), RSL ID (from <em>section</em>)

# Each PDF holds the remaining data we're after (address, e-mail data)

#test with one PDF first:
pdfurl = "https://rsr.tenantservicesauthority.org/RSRDocuments/Download?path=RSLReports%5C2010%5CSL3344.pdf&DocumentId=-2147483648&RSLNumber=SL3344"

#This = FAIL due to https...  Error message:
#HTTPS/1.0 403 Scraperwiki blocked access to "https%3A//rsr.tenantservicesauthority.org/RSRDocum... Error code explanation: 403 = Request forbidden -- authorization will not help.

#test with one I'm hosting to get code for scraper working
pdfurl = "http://alexskene.com/SL3344.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
#DEBUG:
print pdfdata 


pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
print pdfxml

fontspecs = { }
pagetexts = [ ]
for page in root:
    assert page.tag == 'page'
    print "page details", page.attrib
    pagetext = [ ]
    for v in page:
        if v.tag == 'fontspec':
            fontspecs[v.attrib.get('id')] = v
        else:
            assert v.tag == 'text'
            text = re.match('<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            pagetext.append((int(v.attrib.get('top')), int(v.attrib.get('width')), text))
    print pagetext[:40]
    pagetexts.append(pagetext)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

# data is from:  https://rsr.tenantservicesauthority.org/RSRDocuments
# GET parameters for each page:  ?year=2010&page=n (1 to 57)
# each page contains a number of repeating UL elements:

#<li>
#
#              <ul class="RSRDataLink">
#
#                   <li class="RSRDataNumber"><a target="_blank" href="/RSRDocuments/Download?path=RSLReports%5C2010%5CSL3344.pdf&DocumentId=-2147483648&RSLNumber=SL3344"><em>SL3344</em></a></li>
#
#                   <li class="RSRDataName">'Johnnie' Johnson Housing Association Limited</li>
#
#                   
#
#                   <li class="RSRDataView"><a href="/RSRDocuments/ShowShortSummary?year=2010&code=SL3344">Summary Report</a></li>
#
#                   
#
#               </ul>
#
#           </li>

# From this need to scrape:  RSL Name (from RSRDataName), RSL ID (from <em>section</em>)

# Each PDF holds the remaining data we're after (address, e-mail data)

#test with one PDF first:
pdfurl = "https://rsr.tenantservicesauthority.org/RSRDocuments/Download?path=RSLReports%5C2010%5CSL3344.pdf&DocumentId=-2147483648&RSLNumber=SL3344"

#This = FAIL due to https...  Error message:
#HTTPS/1.0 403 Scraperwiki blocked access to "https%3A//rsr.tenantservicesauthority.org/RSRDocum... Error code explanation: 403 = Request forbidden -- authorization will not help.

#test with one I'm hosting to get code for scraper working
pdfurl = "http://alexskene.com/SL3344.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
#DEBUG:
print pdfdata 


pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
print pdfxml

fontspecs = { }
pagetexts = [ ]
for page in root:
    assert page.tag == 'page'
    print "page details", page.attrib
    pagetext = [ ]
    for v in page:
        if v.tag == 'fontspec':
            fontspecs[v.attrib.get('id')] = v
        else:
            assert v.tag == 'text'
            text = re.match('<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            pagetext.append((int(v.attrib.get('top')), int(v.attrib.get('width')), text))
    print pagetext[:40]
    pagetexts.append(pagetext)
    
    
    
