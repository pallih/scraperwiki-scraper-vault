import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

#pdfurl = "http://www.obairs.com/11.pdf"
pdfurl = "http://grff.in/out.pdf"
#pdfurl = "http://www.vdi-nachrichten.com/_library/content/download/obj1382_Tabelle_N.pdf"
#pdfurl = "http://www.bad-schussenried.de/publishNews/redirect.php?id2=13015&id=2210-1305524807-0.pdf" #Gemeindeblatt Schussenkaff
# (harder example to work on: http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf )

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

fontspecs = { }
pagetexts = [ ]

for page in root:
    assert page.tag == 'page'
    pagelines = { }
    for v in page:
        if v.tag == 'fontspec':
            fontspecs[v.attrib.get('id')] = v
        else:
            assert v.tag == 'text'
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            print text #
            top = int(v.attrib.get('top'))
            if top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append((int(v.attrib.get('left')), text))
    lpagelines = pagelines.items()
    lpagelines.sort()
#:100 defines the number of lines to be read
    for top, line in lpagelines[:100]:
#    for top, line in lpagelines[:99999]:
        line.sort()
#        regex = "\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)"
#        r = re.search("^\[\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)", line).group
#        print r 

#373 [(58, '548'), (119, 'Enrique Jerez Garc&#237;a'), (352, 'ESP'), (413, '35-39'), (474, '01:17:14'), (535, '11:16'), (585, ' '), (646, '00:00'), #(695, '00:00:00')]

#        print top, line   
#    pagetexts.append(pagelines)
    # scraperwiki.sqlite.save(data={'line ': line})    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

#pdfurl = "http://www.obairs.com/11.pdf"
pdfurl = "http://grff.in/out.pdf"
#pdfurl = "http://www.vdi-nachrichten.com/_library/content/download/obj1382_Tabelle_N.pdf"
#pdfurl = "http://www.bad-schussenried.de/publishNews/redirect.php?id2=13015&id=2210-1305524807-0.pdf" #Gemeindeblatt Schussenkaff
# (harder example to work on: http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf )

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

fontspecs = { }
pagetexts = [ ]

for page in root:
    assert page.tag == 'page'
    pagelines = { }
    for v in page:
        if v.tag == 'fontspec':
            fontspecs[v.attrib.get('id')] = v
        else:
            assert v.tag == 'text'
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            print text #
            top = int(v.attrib.get('top'))
            if top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append((int(v.attrib.get('left')), text))
    lpagelines = pagelines.items()
    lpagelines.sort()
#:100 defines the number of lines to be read
    for top, line in lpagelines[:100]:
#    for top, line in lpagelines[:99999]:
        line.sort()
#        regex = "\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)"
#        r = re.search("^\[\(\d+, '(\d+)'\), \(\d+, '(\d+)'\), \(\d+, '(.+?)'\), \(\d+, '(\w+)'\), \(\d+, '(.+?)'\)", line).group
#        print r 

#373 [(58, '548'), (119, 'Enrique Jerez Garc&#237;a'), (352, 'ESP'), (413, '35-39'), (474, '01:17:14'), (535, '11:16'), (585, ' '), (646, '00:00'), #(695, '00:00:00')]

#        print top, line   
#    pagetexts.append(pagelines)
    # scraperwiki.sqlite.save(data={'line ': line})    
    
    
