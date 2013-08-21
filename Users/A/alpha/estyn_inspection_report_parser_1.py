import scraperwiki
import urllib, urllib2
import lxml.etree, lxml.html
import re, os

 
def extract_grades(raw):
    """ return a dict mapping key questions to grades awarded """

    rowpat = r'(?:(\d)\s*(.*?)$\s*(\d)\s*$\s*)'
    pat = re.compile(r'Key Question\s+(?:Inspection\s+)?grade\s+.*?' + rowpat*7, re.DOTALL|re.MULTILINE|re.IGNORECASE)
    m=pat.search(raw)
    #print m.groups()

    grades = {}
    for i in range(7):
        qnum = int(m.group(1+i*3))
        q = ' '.join(m.group(2+i*3).split())
        grade = int(m.group(3+(i*3)))
        grades[qnum] = grade

    return grades



def extract_date(raw):
    
    pat = re.compile(r"Date of Inspection:\s*(.*?)\s*$",re.IGNORECASE)
    m = pat.search(raw)
    if m:
        return m.group(1)
    else:
        return ''


def do_it(pdfurl):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div.
    '''

    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)

    # just turn it into plain text
    raw = ''
    for index, page in enumerate(root):
        for text in page:
            raw += ' '.join(text.xpath("descendant-or-self::text()"))
            raw += "\n"

    # pull out the grades
    data = {}
    grades = extract_grades(raw)
    for i in range(1,8):
        data['key_question_grade_%d'%(i,)] = grades[i]
    data['date_of_inspection'] = extract_date(raw)

    return data


#url = "http://www.estyn.gov.uk/download/publication/12694.5/inspection-reportabercerdin-primary-schooleng2008/"

test_reports = [ 
    "http://www.estyn.gov.uk/download/publication/31040.1/inspection-reportcardiff-high-schooleng2007/",
    "http://www.estyn.gov.uk/download/publication/32732.7/inspection-reportcathays-high-schooleng2007/",
    "http://www.estyn.gov.uk/download/publication/20120.1/inspection-reportthe-bishop-of-llandaff-ciw-high-schooleng2005/",
    "http://www.estyn.gov.uk/download/publication/17444.7/inspection-reportargoed-schooleng2009/",
    ]


def Main():
    for line in scraperwiki.datastore.getData("welsh_school_finder", offset=1000):
        if not line['report']:
            continue
        id = line['id']
        if not re.compile('^\d+$').match(id):
            print "skip id=",id
            continue

        report_url = line['report']
#        if report_url not in test_reports:
#            print "skip (not test)"
#            continue
  
        try:
            data = do_it(report_url)
            print report_url, data

            data.update(line)
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        except Exception,e:
            print "FAILED: ", report_url

Main()

