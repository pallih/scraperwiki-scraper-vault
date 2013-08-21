# Copied from ScraperWiki PDF scraping tutorial
# TODO
# Sort address values to write address to db - see http://stackoverflow.com/questions/9001509/python-dictionary-sort-by-key
# Write out key/value pairs as database fields
# Make sure that last tag found doesn't actually belong to next library

import scraperwiki
import urllib2
import lxml.etree
import collections
import re

url = "http://www.bl.uk/reshelp/atyourdesk/docsupply/help/replycodes/dirlibcodes/DLC%20MAY%20pdf.pdf"
pdfdata = urllib2.urlopen(url).read()
#print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
#print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

#print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# print the first element on each page
for page in pages:
    pagenumber=int(page.attrib.get("number"))
    #loop looking for tag with attribute left==46 - this is a library code
    #check if the item before it has top attribute of codetop-3 - if so it is in this block
    #keep looping use the 'left' attribute to group fieldnames and values
    #when hit next library code, process data in hand and write to database
    for i,txt in enumerate(page is not None and page.xpath('text')):
        leftpos=int(txt.attrib['left'])
        toppos = int(txt.attrib['top'])
        if leftpos == 46:
            if 'Library' in locals():
                # Already have a Library object, can use to generate the record
                del Library['Codetop']
                Record = {}
                address = ''
                for k,v in Library.iteritems():
                    if k == "Address":
                        # sort address fields and output
                        oa = collections.OrderedDict(sorted(v.items()))
                        for koa,voa in oa.iteritems():
                            address += voa + ', '
                            if re.match('(GIR 0AA)|((([A-Z][0-9][0-9]?)|(([A-Z][A-Z][0-9][0-9]?)|(([A-Z][0-9][A-HJKSTUW])|([A-Z][A-Z][0-9][ABEHMNPRVWXY])))) ?[0-9][A-Z]{2})',voa):
                                Record.update({'Postcode' :voa})
                                print voa
                        Record.update({'Address' : address.rstrip(' ,')})
                    elif k == "Name":
                        Record.update({'Name' :v})
                    elif k == "Code":
                        Record.update({'Code' :v})
                    elif v.get('label') and v.get('value'):
                        Record.update({v['label'] :v['value']})
                    else:
                        print v
                scraperwiki.sqlite.save(unique_keys=["Code"],data=Record)
            # Create a new Library object as we are starting again
            Library = {}
            Library={'Code' :txt.text.strip()}
            Library.update({'Codetop' :txt.attrib['top']})
            if int(page.xpath('text')[i-1].attrib['top']) == toppos-3:
                Library.update({page.xpath('text')[i-1].attrib['top']: {'value' :page.xpath('text')[i-1].text.strip()}})
            #Library.update({'Policy' :(page is not None and page.xpath('text'))[i-1].text.strip()})
        else:
            if 'Library' in locals():
                if leftpos == 503:
                    if Library.get(str(toppos)):
                        Library[str(toppos)].update({'label' :txt.text.strip().rstrip(':')})
                    else:
                        Library.update({str(toppos) :{'label' :txt.text.strip().rstrip(':')}})
                elif leftpos == 566:
                    if Library.get(str(toppos)):
                        Library[str(toppos)].update({'value' :txt.text.strip()})
                    else:
                        Library.update({str(toppos) :{'value' :txt.text.strip()}})
                if leftpos == 141:
                    if Library.get('Address'):
                        Library['Address'].update({str(toppos) :txt.text.strip()})
                    else:
                        Library.update({'Address' :{str(toppos) :txt.text.strip()}})
                if txt.attrib['top']==Library['Codetop']:
                    Library.update({'Name' :txt.text.strip()})
