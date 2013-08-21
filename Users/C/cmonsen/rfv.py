import scraperwiki
import urllib2
import lxml.etree

url = "http://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/doc08.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

orderedels = []
for page in pages[152:169]:
    leftcol = []
    rightcol = []
    for el in list(page):
        if el.tag == "text" and int(el.get("left")) < 300:
            leftcol.append(el)
        elif el.tag == "text":
            rightcol.append(el)
    orderedels.extend(leftcol)
    orderedels.extend(rightcol)

ccount = 1
scount = 1
codes = []
syns = []
addenda = [
    'pain, ache, soreness, discomfort',               #1
    'cramps, contractures, spasms',                   #2
    'limitation of movement, stiffness, tightness',   #3
    'weakness',                                       #4
    'swelling',                                       #5
    'lump, mass, tumor']                              #6
for el in orderedels:
    if el.text is not None and not not el.text.strip() and el.text.strip()[0].isdigit() and el.text != '1210.0)' and el.text != '1335.0)' and el.text[0:5] != '1900-' and el.text.strip() != '1160.6)':
        wssplit = el.text.strip().split(' ')
        if float(wssplit[0]) > 2000:
            continue
        nextel = orderedels[orderedels.index(el)+1]
        if  len(wssplit) > 1:
            code = wssplit[0]
            name = ' '.join(wssplit[1:])
            if nextel.text is not None and nextel.text[0].islower():
                name += ' ' + nextel.text
        else:
            code = wssplit[0]
            name = nextel.text.strip()
        
            
        foundincl = False
        while nextel.text is not None:
            if nextel.text[0].isdigit() or nextel.text[0:4]=='  Ex':
                break
            elif foundincl:
                syns.append({"rfvid":ccount, "name":nextel.text.strip(), "id":scount})
                scount += 1            
            elif nextel.text[0:4] == '  In':
                foundincl = True
            nextel = orderedels[orderedels.index(nextel)+1]
        
        code = code.strip().replace('.','')
        codes.append({"code":code, "name":name.strip(), "id":ccount})
        ccount += 1
        print codes[-1]

        # Certain codes get auto-generated rfv codes
        if code in map(str,range(19000,19701)):
            for i, s in zip(range(len(addenda)), addenda):
                codes.append({"code":str(int(code)+i+1),"name":name.strip()+": "+s,"id":ccount})
                ccount+=1
            
scraperwiki.sqlite.save(["id"], codes, table_name='rfvs')
scraperwiki.sqlite.save(["id"], syns, table_name='syns')

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

