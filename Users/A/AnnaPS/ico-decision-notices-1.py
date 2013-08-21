# Asking: which authorities have most complaints.
# Which most complaints upheld.
# Which sections of FOIA most referred to and upheld.
# Could cross-reference to WDTK, OpenlyLocal etc.
import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

scraperwiki.metadata.save('data_columns', ['ref_no','authority','date','finding','summary','notice_link', 'pdf_link'])

base_url = "http://www.ico.gov.uk"
starting_page = base_url + "/tools_and_resources/decision_notices.aspx"

# Utility function: strip HTML tags, and leading colons/space.
def tidy_up(data):
    data = data.strip()
    if data[0]==":":
        data=data[1:].strip()
    p = re.compile(r'<[^<]*?>')
    clean_data = p.sub('', data)
    return clean_data

# Scrape individual page containing a month's decision notices.
def scrape_page(notices_page):
    notices_url = base_url + notices_page
    html = scraperwiki.scrape(notices_url)

    # Converts the HTML into a BeautifulSoup object, making it easier to work with.
    # Decode from UTF8 and turn HTML entities into text: BeautifulSoup gives us Unicode back.
    soup = BeautifulSoup(html.decode('utf8'), convertEntities=BeautifulSoup.HTML_ENTITIES)
    notices = soup.find("div", {"class" : "middlecontent"})

    # Get contents of 'notices' (which is a special BeautifulSoup object) as a string. 
    contents = (notices.renderContents()) 

    # Split at each mention of Case Ref to create a new list of cases.
    cases = contents.split(">Case Ref: ")

    for case in cases:
        print case

        # Creates an empty dictionary - 'record' - where we will save info about this case.
        record = {} 
        record['notice_link'] = notices_url 

        # This uses the regex library to search each 'case' for the phrase in brackets. 
        # With ^ to indicate this must be at start of the string, .*? as a wildcard
        # afterwards, then < to close the search when it meets the first HTML tag.
        # Assert if we find a paragraph that isn't just empty HTML.
        case_ref = re.search("(^(FS|FER|FAC).*?)<", case)
        if case_ref:
            record['ref_no'] = case_ref.group(1).strip()
        else:
            case += ">"
            assert ((tidy_up(case).strip()=="") or ("Please find below" in case)) 
            continue

        public_authority = re.search("Authority(.*?)(<br|<p)", case, re.DOTALL)
        record['authority'] = tidy_up(public_authority.group(1).strip())

        # Now again for the findings. Skip the one case that doesn't have one.
        # Findings are indicated in numerous different ways: we handle all of them. 
        if record['ref_no'] == "FS50082845":
            record['finding'] = "None listed"
        else: 
            #findings = re.search("(Finding|Section of Act: FOI|Section of Act/EIR & Finding|Section of (the )?Act(.*?):)(.*?)(<br|<p|$)", case, re.DOTALL)
            findings = re.search("(Finding|Section of Act: FOI|Section of Act/EIR & Finding|Section of (the )?Act(.*?):)(.*?)(<a|<p)", case, re.DOTALL)
            findings = tidy_up(findings.group(4).strip())
            findings = [f.strip() for f in (re.split(r';|,', findings))]
            #for i, f in enumerate(findings):
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

        # Get the PDF link - which may actually be an .ashx link - and add domain if needed. 
        pdf_link = re.search("href=[\"|'](.*?(pdf|ashx|aspx))", case)
        pdf_link = pdf_link.group(1).strip()
        if pdf_link[0]=="~":
            pdf_link = pdf_link[1:]
        if "ico.gov.uk" not in pdf_link:
            pdf_link = "http://www.ico.gov.uk" + pdf_link
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


# Function to convert decision notices starting page to soup object so we can go to links.
def find_the_list(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    # GRAB the list of links to monthly decision notices
    # Look at the HTML for the tag containing all the information.
    # <a> isn't as good because it's closed before the information is all used.
    # <div> isn't as good because there's other information in it.
    # There is only one instance of the <li> class below, which is key.
    # Finding <li class="open"> then the ul within that, then all the <li> within that.
    notices_links = soup.find("li", {"class" : "open"}).find("ul").findAll("li")
    for link in notices_links:
        # We can uncomment this line to scrape only one year if we want, for testing purposes.
        #if ("2010" in str(link)):
            #continue  
        print "Scraping %s" % link.text
        notices_page = link.find("a")['href']
        scrape_page(notices_page)

find_the_list(starting_page)
