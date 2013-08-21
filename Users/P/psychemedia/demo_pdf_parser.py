import scraperwiki
import urllib2, lxml.etree


url='http://data.gov.uk/sites/default/files/ODUG%20Applications%202012.pdf'

pdfdata = urllib2.urlopen(url).read()

xmldata = scraperwiki.pdftoxml(pdfdata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)


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
    return "".join(res).strip()

headings={'Name':'name', "Job title(s) and orgnisation(s)":'jobOrg', 'Which of the following types of organisation will you be able to represent?':'represent', 'Why do you feel you will be able represent these organisations?':'whyOrg', 'Which of the following industries/sectors will you be able to represent?':'indSector', 'Why do you feel you will be able to represent this industry?':'whyIndustry','Which of the following skills will you be able to bring to the ODUG membership?':'skills', 'Please give evidence for this skill:':'evidence', 'Are there any other reasons why you would like to become a member of ODUG?':'otherReasons', 'Are you currently a member of any other organisation(s) in a similar or related field?':'otherOrgs', 'If yes which organisation(s):':'yesOrgs','Will you be sending any additional information to support this application which you would like to keep private?':'additionalInfo'}

bigdata=[]

print pages
for page in pages:
    data={}
    for el in page:
        if el.tag == "text":
            if el.attrib['top']=='1220': pass
            else:
                #HorribleHack - there must be a better way of dealing with this?
                val=gettext_with_bi_tags(el).encode('utf8').replace('\xc2\xa0',' ')
                #val=gettext_with_bi_tags(el)
                if val in headings:
                    #print '..',headings[val],
                    keyval=headings[val]
                    data[ keyval ]=''
                elif data!={}: 
                    #print val
                    data[ keyval ] = ' '.join( [ data[ keyval ], val ] )
    bigdata.append(data)

for data in bigdata:
    print data
    #scraperwiki.sqlite.save(unique_keys=['name'], table_name='odugUK_apps_2012', data=data)
