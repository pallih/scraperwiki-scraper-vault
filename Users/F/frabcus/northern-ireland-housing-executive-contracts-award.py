import tempfile
import urllib
import scraperwiki
import os
import re
import datetime
import lxml.etree, lxml.html

def pdftotxt(pdfdata):
    """converts pdf file to txt file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    print pdffout.name
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    #cmd = '/usr/bin/pdftohtml -nodrm -enc UTF-8 "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

def remove_html_tags(data):
    data = data.replace("&amp;", "&")
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def gen_raw_lines(lines):  
    last_top = None
    merged_line = ""
    for line in lines:
        if "<text" not in line:
            continue

        matches = re.search('top="(\d+)"', line)
        top = int(matches.groups(1)[0])
        #print top
        if top <> last_top:
            yield merged_line
            merged_line = ""
        merged_line = merged_line + remove_html_tags(line)
        last_top = top
    if merged_line != "":
        yield merged_line

def do_one_pdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    txt = pdftotxt(pdfdata)
    print txt
    #return
    
    contractors = {}
    gen = gen_raw_lines(txt.split("\n"))
    for line in gen:
        
        if "CONTRACTOR:" in line:
            contractor_number = int(line[12:17].strip())
            name = line[17:].strip()
            addr2 = gen.next()
            addr3 = gen.next()
            addr4 = gen.next()
            if addr4.strip() == '':
                addr = addr2.strip() + ", " + addr3.strip()
            else:
                addr5 = gen.next()
                if addr5.strip() == '':
                    addr = addr2.strip() + ", " + addr3.strip() + ", " + addr4.strip()
                else:
                    raise Exception("not three/four line address after " + line)
            if contractor_number in contractors:
                raise Exception("error, found address record for same contractor twice in one PDF")
            contractors[contractor_number] = (name, addr)
        
        elif re.match('^\d{7}', line):
            print line

            # one off patches
            if "0161068     DRUMLECK DRIVE" in line:
                line = line.replace("0161068     DRUMLECK DRIVE", "0161068        DRUMLECK DRIVE")
    
            project_number = line[0:7].strip()
            scheme = line[8:39].strip()
            work_category = line[39:70].strip()
            contractor_number = int(line[70:75].strip())
            date_of_possession = line[75:87].strip()
            tender_cost = line[87:99].strip()
            duration = line[99:109].strip()
            number_dwellings = line[109:].strip()
    
            (day, month, year) = date_of_possession.split("/")
            (contractor_name, contractor_address) = contractors[contractor_number]
            
            record = { 'project_number': project_number,
                       'scheme': scheme,
                       'work_category': work_category,
                       'contractor_number': contractor_number,
                       'contractor_name': contractor_name,
                       'contractor_address': contractor_address,
                       'date_of_possession': date_of_possession,
                       'tender_cost': tender_cost,
                       'duration': duration,
                       'number_dwellings': number_dwellings
            }
            print record
            scraperwiki.datastore.save(unique_keys=['project_number'], data=record, date=datetime.date(2000 + int(year), int(month), int(day)))
    
        
        else:
            #print "UNUSED: ", line
            pass

do_one_pdf('http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf')

    
url = "http://www.nihe.gov.uk/index/wwu_home/procurement/tenders/contracts_awarded.htm"
root = lxml.html.parse(url).getroot()

for a in root.cssselect('html body div#iewrap div#mainwrap div#wrap1 div#wrap2 div#content p a'):
    if a.get('href') != 'contracts_awarded_-_sept_2010.pdf': # ignore this one for now
        pdf_url = "http://www.nihe.gov.uk/" + a.get('href')
        print "-----------------------------------"
        print "Parsing:", pdf_url

        do_one_pdf(pdf_url)


import tempfile
import urllib
import scraperwiki
import os
import re
import datetime
import lxml.etree, lxml.html

def pdftotxt(pdfdata):
    """converts pdf file to txt file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    print pdffout.name
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    #cmd = '/usr/bin/pdftohtml -nodrm -enc UTF-8 "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

def remove_html_tags(data):
    data = data.replace("&amp;", "&")
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def gen_raw_lines(lines):  
    last_top = None
    merged_line = ""
    for line in lines:
        if "<text" not in line:
            continue

        matches = re.search('top="(\d+)"', line)
        top = int(matches.groups(1)[0])
        #print top
        if top <> last_top:
            yield merged_line
            merged_line = ""
        merged_line = merged_line + remove_html_tags(line)
        last_top = top
    if merged_line != "":
        yield merged_line

def do_one_pdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    txt = pdftotxt(pdfdata)
    print txt
    #return
    
    contractors = {}
    gen = gen_raw_lines(txt.split("\n"))
    for line in gen:
        
        if "CONTRACTOR:" in line:
            contractor_number = int(line[12:17].strip())
            name = line[17:].strip()
            addr2 = gen.next()
            addr3 = gen.next()
            addr4 = gen.next()
            if addr4.strip() == '':
                addr = addr2.strip() + ", " + addr3.strip()
            else:
                addr5 = gen.next()
                if addr5.strip() == '':
                    addr = addr2.strip() + ", " + addr3.strip() + ", " + addr4.strip()
                else:
                    raise Exception("not three/four line address after " + line)
            if contractor_number in contractors:
                raise Exception("error, found address record for same contractor twice in one PDF")
            contractors[contractor_number] = (name, addr)
        
        elif re.match('^\d{7}', line):
            print line

            # one off patches
            if "0161068     DRUMLECK DRIVE" in line:
                line = line.replace("0161068     DRUMLECK DRIVE", "0161068        DRUMLECK DRIVE")
    
            project_number = line[0:7].strip()
            scheme = line[8:39].strip()
            work_category = line[39:70].strip()
            contractor_number = int(line[70:75].strip())
            date_of_possession = line[75:87].strip()
            tender_cost = line[87:99].strip()
            duration = line[99:109].strip()
            number_dwellings = line[109:].strip()
    
            (day, month, year) = date_of_possession.split("/")
            (contractor_name, contractor_address) = contractors[contractor_number]
            
            record = { 'project_number': project_number,
                       'scheme': scheme,
                       'work_category': work_category,
                       'contractor_number': contractor_number,
                       'contractor_name': contractor_name,
                       'contractor_address': contractor_address,
                       'date_of_possession': date_of_possession,
                       'tender_cost': tender_cost,
                       'duration': duration,
                       'number_dwellings': number_dwellings
            }
            print record
            scraperwiki.datastore.save(unique_keys=['project_number'], data=record, date=datetime.date(2000 + int(year), int(month), int(day)))
    
        
        else:
            #print "UNUSED: ", line
            pass

do_one_pdf('http://www.nihe.gov.uk/schemes_accepted_010109_to_310309.pdf')

    
url = "http://www.nihe.gov.uk/index/wwu_home/procurement/tenders/contracts_awarded.htm"
root = lxml.html.parse(url).getroot()

for a in root.cssselect('html body div#iewrap div#mainwrap div#wrap1 div#wrap2 div#content p a'):
    if a.get('href') != 'contracts_awarded_-_sept_2010.pdf': # ignore this one for now
        pdf_url = "http://www.nihe.gov.uk/" + a.get('href')
        print "-----------------------------------"
        print "Parsing:", pdf_url

        do_one_pdf(pdf_url)


