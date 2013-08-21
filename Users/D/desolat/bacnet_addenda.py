import scraperwiki
from lxml.html.soupparser import fromstring
from lxml import etree
import urllib
import urllib2
import re
import StringIO
import sys
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTTextLineHorizontal, LTTextBoxHorizontal, \
                            LTChar, LTRect, LTLine, LTAnon
import pprint 

STATE = {
        'approved' : 'approved',
        'review' : 'review'
        }


def extractLinesText(layout):
    tlines = [ ]  
    objstack = list(reversed(layout._objs))
    xlines = [ ]  # (x0,y0,x1,y1)  
    ylines = [ ]  # (x0,y0,x1,y1)  
    while objstack:
        b = objstack.pop()
        if type(b) in [LTFigure, LTTextBox, LTTextLine, LTTextBoxHorizontal]:
            objstack.extend(reversed(b._objs))
        elif type(b) == LTTextLineHorizontal:
            tlines.append(b)
        elif type(b) == LTLine: # build up a list of perpendicular lines
            if b.x0 == b.x1:
                xlines.append((b.x0,b.y0,b.x1,b.y1))
            elif b.y0 == b.y1:
                ylines.append((b.x0,b.y0,b.x1,b.y1))
            else:
                print "slopy", b
        elif type(b) == LTRect: # rectangles are basically four lines
            xlines.append((b.x0,b.y0,b.x0,b.y1,0))
            ylines.append((b.x0,b.y0,b.x1,b.y0,0))
            xlines.append((b.x1,b.y0,b.x1,b.y1,1))
            ylines.append((b.x0,b.y1,b.x1,b.y1,1))
    return xlines, ylines, tlines


def processAddendaPdf(absDocUrl):
    print 'Parsing addenda pdf %s ...' % absDocUrl
    pdfbin = urllib.urlopen(absDocUrl).read()
    cin = StringIO.StringIO()
    cin.write(pdfbin)
    cin.seek(0)
    parser = PDFParser(cin)
    doc = PDFDocument()
    parser.set_document(doc)
    try:
        doc.set_parser(parser)
    
        doc.initialize()
        
        assert doc.is_extractable
    
    #    outlines = doc.get_outlines()
    #    for (level,title,dest,a,se) in outlines:
    #        print (level, title)
    
        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        revHistFound = False
        revision = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            xlines, ylines, tlines = extractLinesText(layout)
            for tline in tlines:
                lineText = tline.get_text()
                #print lineText
                if not revHistFound:
                    match = re.match('.*HISTORY OF REVISIONS.*', lineText)
                    if match:
                        revHistFound = True
                        print 'Revision History found'
                else:
                    match = re.match('(?P<version_info>\d+)\s*', lineText)
                    if match:
                        versionInfo = match.group('version_info')
                        revision.append(versionInfo)
                        if len(revision) == 2:
                            break
            if len(revision) > 0:
                break
    
        if len(revision) < 2:
            raise BaseException('Could not find revision info')
        else:
            revision = '.'.join(sorted(revision))

    except BaseException as e:
        print 'ERROR: %s' % str(e)
        revision = 'ERROR while parsing the PDF: %s' % str(e)

    print 'Revision: %s' % revision
    data = {'revision' : revision}
    return data


scraperwiki.sqlite.execute("create table if not exists addenda (id text, revision text)")
url = 'http://www.bacnet.org/Addenda/index.html'
base, page = url.rsplit('/', 1)
h = urllib2.urlopen(url)
doc = fromstring(h.read())
root = doc
tables = root.cssselect('table')
addendaTable = tables[1]
addendaLists = addendaTable.cssselect('ul')

for addendaList in addendaLists:
    addendaId = None
    standard = None
    absDocUrl = None
    topics = None
    state = None
    comment = None
    for child in addendaList:
        #print child.tag
        if child.tag == 'li':
            links = child.cssselect('a')
            assert len(links) == 1, 'Found %d a tags in the addenda list item' % len(links)
            relDocUrl = urllib.quote(links[0].attrib.get('href'))
            
            idPatterns = [
                          'Add-(?P<year>[0-9]{4})-(?P<ashrae_id>[0-9.]+)(?P<ashrae_ext>[a-z]+).*',
                          'Add-(?P<year>[0-9]{4})-(?P<ashrae_id>[0-9.]+)-(?P<ashrae_sub_id>[0-9]+)-(?P<ashrae_ext>[a-z]+).*',
                          'Add-(?P<ashrae_id>[0-9]{3})-(?P<year>[0-9]{4})(?P<ashrae_ext>[a-z]+).*',
                          'Add-(?P<ashrae_id>[0-9]{3})[_-](?P<ashrae_sub_id>[0-9]+)-(?P<year>[0-9]{4})(?P<ashrae_ext>[a-z]+).*',
                          ]
            for idPattern in idPatterns:
                idMatch = re.match(idPattern, relDocUrl, re.I)
                if idMatch:
                    if idMatch.groupdict().has_key('ashrae_sub_id'):
                        standard = '%s.%s' % (idMatch.group('ashrae_id'), idMatch.group('ashrae_sub_id'))
                    else:
                        standard = idMatch.group('ashrae_id')
                    addendaId = '%s-%s%s' % (standard, idMatch.group('year'), idMatch.group('ashrae_ext'))
                    break
            if not standard:
                raise BaseException('Could not match %s' % relDocUrl)

            absDocUrl = ('/'.join((base, relDocUrl)))
            print 'Doc URL: %s' % absDocUrl
            comment = links[0].tail            
            if comment is not None:
                comment = comment.strip('() ')
                #print comment
                reviewMatch = re.match('.*review.*', comment, re.I)
                if reviewMatch:
                    state = STATE['review']
                else:
                    approvedMatch = re.match('.*approved.*', comment, re.I)
                    if approvedMatch:
                        state = STATE['approved']
                    else:
                        raise BaseException('Could not find status for %s' % addendaId)
            else:
                comment = ''
                state = STATE['approved']
    
#        elif child.tag == 'a':
#            if child.attrib.has_key('name'):
#                addendaId = child.attrib['name']
#                print 'Addenda ID: %s' % addendaId
        elif child.tag == 'ol':
            topicItems = child.cssselect('li')
            topics = {}            
            for index, topicItem in enumerate(topicItems, start=1):
                topics[index] = topicItem.text

        if addendaId and absDocUrl and topics and state and standard:
            data = scraperwiki.sqlite.select("* from addenda where id=?", [addendaId])
            print data
            if len(data) > 1:
                raise BaseException('ID %s should be unique but was found %d times' % (addendaId, len(data)))
            elif len(data) < 1:
                data = {}
            else:
                data = data[0]

            data.update({
                        'id' : addendaId,
                        'standard' : standard,
                        'doc_url' : absDocUrl,
                        'topics' : topics,
                        'state' : state,
                        'comment' : comment,
                        })

            if state == STATE['approved'] and standard == '135' and (not data.has_key('revision') or 
                                               data['revision'] is None or
                                               data['revision'].startswith('ERROR')):
                pdfData = processAddendaPdf(absDocUrl)
                data.update(pdfData)

            print 'Saving data %s ...' % str(data)
            # @todo: existing items should be updated
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='addenda')
            addendaId = None
            standard = None
            absDocUrl = None
            topics = None
            state = None
            comment = None
    
            

