import scraperwiki
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer

scraperwiki.metadata.save('data_columns', ['ref_no','authority','date','finding','summary','pdf_link'])

#tidy content

def tidy_up(data):
    data = data.strip()
    if data[0]==":":
        data=data[1:].strip()
    p = re.compile(r'<[^<]*?>')
    clean_data = p.sub('', data)
    return clean_data

#scrap the list page an convert
html = scraperwiki.scrape('http://www.ico.org.uk/enforcement/decision_notices/decision_notice_list.html')
soup = BeautifulSoup(html.decode('utf8'), convertEntities=BeautifulSoup.HTML_ENTITIES)
notices = soup.find("div", {"class" : "middlecontent"})

#get contents of 'notices
contents = (notices.renderContents())
cases = contents.split(">Case Ref: ")
for case in cases: print case

        # Creates an empty dictionary - 'record' - where we will save info about this case.
record = {} 
record['notice_link'] = html 

        # This uses the regex library to search each 'case' for the phrase in brackets. 
        # With ^ to indicate this must be at start of the string, .*? as a wildcard
        # afterwards, then < to close the search when it meets the first HTML tag.
        # Assert if we find a paragraph that isn't just empty HTML.
case_ref = re.search("(^(FS|FER|FAC).*?)<", case)
if case_ref:
    record['ref_no'] = case_ref.group(1).strip()
else:
            case += ">"

public_authority = re.search("Authority(.*?)(<br|<p)", case, re.DOTALL)
record['authority'] = tidy_up(public_authority.group(1).strip())

        # Now again for the findings. Skip the one case that doesn't have one.
        # Findings are indicated in numerous different ways: we handle all of them. 
if record['ref_no'] == "FS50082845":
    record['finding'] = "None listed"
else: 
    findings = re.search("(Finding|Section of Act: FOI|Section of Act/EIR & Finding|Section of (the )?Act(.*?):)(.*?)(<a|<p)", case, re.DOTALL)
findings = tidy_up(findings.group(4).strip())
findings = [f.strip() for f in (re.split(r';|,', findings))]
if f: 
    finding = f.replace(".","").title()
if finding[0]==":":
                finding = finding[1:].strip()
                finding = finding.replace(" "," ").replace("Partially","Partly")
                finding = finding.replace("Complaint ","").replace("Compliant ","")
                finding = finding.replace(" -",":").replace(" –",":").strip()
                print finding
                record['findings'] = finding.strip()

        # Get the date. Deal with the case with no date!
if record['ref_no'] == "FS50068236":
            record['date'] = "20/07/05"
else:
            date_of_decision = re.search("Date:(.*?)(<br|<p)", case, re.DOTALL)
            record['date'] = tidy_up(date_of_decision.group(1).strip())

        # Get the summary - again listed in numerous different ways. 
summary = re.search("Summary(.*?)(Section of Act|Section of the Ac|Case of Act|Full Transcript)", case, re.DOTALL)
record['summary'] = tidy_up(summary.group(1).strip())

#get PDF

pdf_link = re.search("href=(.*?(pdf|ashx|aspx))", case, re.DOTALL)
pdf_link = pdf_link.group(1).strip()
if pdf_link[0]=="~":
    pdf_link = pdf_link[1:]
if "ico.org.uk" not in pdf_link:
    pdf_link = "http://www.ico.org.uk" + pdf_link
    record['pdf_link'] = pdf_link

        # We have got all our information. Save record to the datastore,
        # with 'ref_no' as the key that is unique to this record.
        #print record
try:
    for k, v in record.items():
                 # Convert everything to Unicode first. 
                 record[k] = unicode(v.decode('utf-8'))
except UnicodeDecodeError:
        print "Record %s, %s was not a utf8-encoded unicode string" % (k,v)
scraperwiki.datastore.save(unique_keys=["ref_no"], data=record)


