import scraperwiki
import urllib2,re
import lxml.etree
from geopy import geocoders  

try:
    scraperwiki.sqlite.execute('drop table "swdata"')
except:
    pass

url = "http://www.direct.gov.uk/prod_consum_dg/groups/dg_digitalassets/@dg/@en/documents/digitalasset/dg_200711.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


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

inContrib=0

#tag stripper via http://love-python.blogspot.com/2008/07/strip-html-tags-using-python.html
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def saveRecord(data):
    location=data["location"].lstrip('(')
    location=location.strip()
    location=location.rstrip(')')
    name=remove_html_tags(data['name'])
    name=name.strip()
    if not name.startswith("New Year") and name[-1].isupper():
        print '>>'+name+'<<'
        scraperwiki.sqlite.save(unique_keys=["skey"], data={"honour":data['honour'], "name":name,"location":location,"contribution":data["contribution"],"skey":data['skey'],"lat":data['lat'],"lng":data['lng'],"place":data["place"]})

def saveRecords(data):
    for record in data:
        if record=='oops':
            print 'oops'
            exit(-1)
        saveRecord(data[record])

#todo ERROR when names over multiple lines eg Una on page 82

g = geocoders.Google()

data={}
honour=''
prevhonour=0
contribution=''
key='oops'
pc=0
# print the first hundred text elements from the first page
for page in pages:
    pc=pc+1
    for el in list(page):
        if el.tag == "text":
            #print el.attrib, gettext_with_bi_tags(el)
            if inContrib==1 and int(el.attrib['left'])<541:
                #print "CONTRIBUTION?",key,contribution
                inContrib=0
                if key not in data: print key,data
                data[key]['contribution']=contribution
                contribution=''
            if el.attrib['font']=='1' and el.attrib['left']=='540':
                #print "LOCATION?", gettext_with_bi_tags(el)
                data[key]['location']=gettext_with_bi_tags(el)
                #place, (lat, lng) = g.geocode(data[key]['location'])
                #data[key]["lat"]=lat
                #data[key]["lng"]=lng
                #data[key]["place"]=place
            if el.attrib['font']=='4' and el.attrib['left']=='89':
                if prevhonour==0:
                    #print "HONOUR?", gettext_with_bi_tags(el)
                    honour=remove_html_tags(gettext_with_bi_tags(el)).strip()
                else: honour=honour+' '+remove_html_tags(gettext_with_bi_tags(el)).strip()
                prevhonour=1
            else: prevhonour=0
            if el.attrib['font']=='1' and int(el.attrib['left'])<120:
                if key in data: print data[key]
                #print "NAME?", gettext_with_bi_tags(el)
                key='p'+str(pc)+str(el.attrib['top'])
                #print 'namekey',key
                data[key]={'name':gettext_with_bi_tags(el),'honour':honour,'location':'','contribution':'','skey':key,'lat':'','lng':'','place':''}
            if el.attrib['font']=='1' and el.attrib['left']=='541':
                #print gettext_with_bi_tags(el),
                inContrib=1
                if contribution=='':
                    key='p'+str(pc)+str(el.attrib['top'])
                    #print 'contributionkey',key
                ctxt=gettext_with_bi_tags(el)
                if ctxt.startswith("("):
                    data[key]["location"]=ctxt
                else:
                    contribution=contribution+ctxt

saveRecords(data)

# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/


