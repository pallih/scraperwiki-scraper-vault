import scraperwiki
import urllib
import lxml.etree, lxml.html
import lxml
import re
import urllib2
from BeautifulSoup import BeautifulSoup

def main():
    main_url = "http://www.supremecourt.gov/opinions/opinions.aspx"
    main_html = urllib2.urlopen(main_url)
    soup = BeautifulSoup(main_html)
    listdivs = soup.findAll('div', {'class':'dslist2'})
    for listdiv in listdivs:
        years = listdiv.find('ul')
        years_links = years.findAll('li')
        desired_link = years_links[0].find('a')['href']
        processSinglePage("http://www.supremecourt.gov/opinions/" + desired_link)

def processSinglePage(main_url):
    main_html = urllib2.urlopen(main_url)
    soup = BeautifulSoup(main_html)

    maindiv = soup.find('div', {'id':'maincontentbox'})
    sc_table = maindiv.find('table')
    sc_rows = sc_table.findAll('tr')

    justice_defs = get_justice_defs() # mappings of abbreviations to names

    for sc_row in sc_rows[1:]:
        cells = sc_row.findAll('td')
        seq_num = cells[0].text
        date_decided = cells[1].text
        docket_number = cells[2].text
        pdf_a = cells[3].find('a')
        pdf_url = ''
        if pdf_a:
            pdf_url = 'http://www.supremecourt.gov/opinions/' + pdf_a['href']
        case_name = pdf_a.text 
        
        justice_abbr = cells[4].text
        principal_justice = ''
        if justice_defs.keys().count(justice_abbr) == 0:
            principal_justice = "No definition found"
            print "WARNING: Cannot find definition for " + justice_abbr
        else:
            principal_justice = justice_defs[justice_abbr]

        # If the case isn't per curiam, scrape the contents of the docket.
        if cells[4].text != 'PC':
            case_info = getCaseInformation(pdf_url)
        # Otherwise, fill in the case_info dictionary with reasonable defaults.
        else:
            case_info = {'dates': {'argued': 'None', 'decided': 'date_decided'}, 'decision': 'None'}

        report_vol = cells[5].text
        case_record = {'sequential_number':seq_num, 'date_decided':date_decided, 'docket_number':docket_number, 
            'case_name':case_name,'principal_justice':principal_justice, 'report_volume':report_vol, 
            'date_argued': case_info['dates']['argued'],
            'decision': case_info['decision']}
        scraperwiki.sqlite.save(['case_name','date_decided','docket_number','case_name','principal_justice',
                                 'report_volume','date_argued','decision'],case_record)
        print case_record

def get_justice_defs():
    definition_urls = ["definitions.aspx", "definitions_a.aspx", "definitions_b.aspx", "definitions_c.aspx", "definitions_d.aspx"]
    justice_defs = {}
    for url in definition_urls:
        definition_url = "http://www.supremecourt.gov/opinions/" + url
        definition_soup = BeautifulSoup(urllib2.urlopen(definition_url)) # TODO check it doesn't fail
        definitions_info = definition_soup.find('div', {'id': 'maincontentbox'}).find('blockquote')
        definitions_txt = definitions_info.__str__()
        justice_abbrs = definitions_info.findAll('b')
        for abbr in justice_abbrs:
            reg_ex = '<b>' + abbr.text + '</b>(.*)<' # ASSUMPTION: no html tags within the justice name
            justice_name = re.search((reg_ex), definitions_txt).group(1).strip()
            abbr_txt = abbr.text[:-1] # won't include the ending colon
            if justice_defs.keys().count(abbr_txt) == 0: # new key
                justice_defs[abbr_txt] = justice_name
            elif justice_defs[abbr_txt] != justice_name: # same abbreviation expands to different justice name. this might be a problem i
                print "WARNING: The principal justice may be wrongly scraped. The abbreviation for their name gets used twice over previous years, breaking an assumption in the parsing code. Sorry :("
    return justice_defs

def textFromNode(node):
    return re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(node)).group(1)

# The main challenge of the code at this point is that if we have a single line of text
# that happens to contain nouns in TITLE CASE, the line is split into multiple different
# pieces of text that don't all exist at the same height.  Our idea will therefore be to
# reassemble these fragments into full pieces of text in order to reduce the complexity
# of finding importance pieces of text.
#
# We will make several assumptions in the course of this document processing which are not
# guaranteed to be valid, but which seem to be an artifact of the PDFs.  I'm basing these
# assumptions on a quick inspection of a few PDFs that I've scraped this way.
#
# The first assumption is that if we need to assemble two or more pieces of text into one
# line, that all of the entries on that line will be within some fixed number of pixels
# of one another.  Consider, for example, this snippet of the generated XML:
#
#    <text top="460" left="156" width="296" height="13" font="4">trial counsel to adopt a family-sympathy mitigation de­</text>
#    <text top="473" left="156" width="304" height="13" font="4">fense.  <i>Post</i>, at 27.  She cites no evidence, however, that </text>
#    <text top="487" left="156" width="304" height="13" font="4">such an approach would have been inconsistent with the </text>
#    <text top="500" left="156" width="300" height="13" font="4">standard of professional competence in capital cases that</text>
#    <text top="513" left="156" width="305" height="13" font="4">prevailed in Los Angeles in 1984.  Indeed, she does not </text>
#    <text top="526" left="156" width="303" height="13" font="4">contest that, at the time, the defense bar in California had </text>
#    <text top="540" left="156" width="305" height="13" font="4">been using that strategy.  See <i>supra</i>, at 19; <i>post</i>, at 28, </text>
#    <text top="553" left="156" width="42" height="13" font="4">n. 21.  J</text>
#    <text top="555" left="198" width="38" height="11" font="0">USTICE </text>
#    <text top="553" left="237" width="7" height="13" font="4">S</text>
#    <text top="555" left="244" width="55" height="11" font="0">OTOMAYOR</text>
#    <text top="553" left="299" width="161" height="13" font="4"> relies heavily on <i>Wiggins</i>, but </text>
#    <text top="568" left="156" width="57" height="11" font="0">—————— </text>
#    <text top="582" left="165" width="7" height="7" font="7">17</text>
#
# Notice that the fragments for JUSTIC SOTOMAYOR all have tops that are within a few pixels of
# one another.
#
# This algorithm works by looking for consecutive blocks of text that can be aggredated together.
# Whenever the next piece of text is found, if its top is not within a set window of pixels
# from that last text shard, we assume it's part of a new line.  Otherwise, it will get globbed
# together with the previous piece of text.

kMaxLineDelta = 2 # Maximum permissible change while staying on the same line.

def getSupremeCourtOpinionPages(pdfurl):   
    # Grab the raw PDF data.
    pdfdata = urllib.urlopen(pdfurl).read()
    
    # Convert it to an XML document.
    pdfxml = scraperwiki.pdftoxml(pdfdata)

    # Parse that XML into an XML document tree.
    root = lxml.etree.fromstring(pdfxml)

    # Scan across the pages, building up each into a list of lines.
    pages = []

    for page in root:
        # Verify that the entry we're looking at is indeed a page.
        assert page.tag == 'page'
            
        # Keep track of the piece of text we've accumulated so far, along with its last position.
        # Initially, this is the empty string at a negative offset, which I presume is not going
        # to exist in a PDF document.
        #
        # In particular, I'm going to set the last Y coordinate to a value so that the difference
        # between that Y coordinate and any Y coordinate we find is at least kMaxLineDelta, which
        # forces a new line.
        lastY = -(kMaxLineDelta + 1)
        text = ""
        
        # Keep track of the lines of text from this page.
        lines = []
        
        # Scan over the page contents, reading lines of text from it.
        for v in page:
            # If this is a text node, we need to extract the text contents from it.
            if v.tag == 'text':
                # See whether this is a continuation of the previous line or the start of a brand-
                # new line.
                yCoord = int(v.attrib["top"])
                
                # If this is a new line, record what we have so far.
                if abs(yCoord - lastY) > kMaxLineDelta:
                    # If there's text at all, append it.  There won't be text in some odd cases
                    # where the text is blank, or at the start of this loop.
                    if text != "":
                        lines.append(text)
                        
                    # Clear the accumulated text.
                    text = ""

                # Append to the accumulated text the text from this fragment.  We also strip leading
                # and trailing whitespace to make it easier to do exact matches on the text.
                text += textFromNode(v).strip()

                # Record where this text occurs.
                lastY = yCoord            

            # Otherwise, we assume it's a font specification.  If this is incorrect, abort execution
            # with an error.
            else:
                assert v.tag == 'fontspec'

        # At the very end, if we have any text accumulated, add it to the list of lines.
        if text != "":
            lines.append(text)

        # Finally, record these lines as being part of the page.
        pages.append(lines)

    return pages

# Detects whether an opinion is a Per Curiam decision or a regular opinion.  This current implementation
# is a Gross Awful Hack that works by noticing that on the first page, Per Curium decisions have the header
# "Per Curiam" on the second line, whereas regular decisions have the header "Syllabus."  I believe that
# this works correctly, but I'm not at all proud of it.  Please feel free to fix this if need be.
def isPerCuriamDecision(pages):
    # Confirm that the pages aren't empty.
    assert len(pages) > 0

    # The first page should have at least two lines, the second of which has the text we want.
    assert len(pages[0]) >= 2

    # We should be seeing either Per Curiam or Syllabus here.
    assert pages[0][1] == "Per Curiam" or pages[0][1] == "Syllabus"

    # Hand back whether this is Per Curiam.
    return pages[0][1] == "Per Curiam"

# A utility function to pad a number to two digits by prepending a zero if necessary.
def padNumber(numberAsString):
    if len(numberAsString) == 1:
        return '0' + numberAsString
    else:
        return numberAsString

# A utility function to convert from the {Month} {Day}, {YYYY} format to the simpler MM/DD/YY format
# used elsewhere in the code.
def dateToMMDDYY(date):
    # Use a regular expression to tease apart the date.
    regResult = re.match('(.*?) (\d*), \d\d(\d\d)', date)
    result = ""

    # Convert the month to a number.
    prettyMonth = regResult.group(1)
    if prettyMonth == "January":
        result += "1"
    elif prettyMonth == "February":
        result += "2"
    elif prettyMonth == "March":
        result += "3"
    elif prettyMonth == "April":
        result += "4"
    elif prettyMonth == "May":
        result += "5"
    elif prettyMonth == "June":
        result += "6"
    elif prettyMonth == "July":
        result += "7"
    elif prettyMonth == "August":
        result += "8"
    elif prettyMonth == "September":
        result += "9"
    elif prettyMonth == "October":
        result += "10"
    elif prettyMonth == "November":
        result += "11"
    elif prettyMonth == "December":
        result += "12"
    else:
        assert False

    # Append the day and the year.
    result += "/" + padNumber(regResult.group(2)) + "/" + padNumber(regResult.group(3))
    return result

# Recovers the "date argued" and "date decided" information about a case.  This information should
# be on the very first page of the case description on its own line.
def getCaseDates(pages):
    # Confirm there's at least one page.
    assert len(pages) > 0

    # Scan across all the lines until we find one that matches the appropriate pattern.
    for line in pages[0]:
        # Look for the match against the pattern here, which finds the "Argued" and "Decided" dates.
        result = re.match(".*Argued\s*(.*)&#\d*;Decided\s*(.*)", line)

        # If we didn't match anything, skip this entry.
        if result == None:
            continue

        # Otherwise, package the result into a nice object and hand it back.
        return {'argued': dateToMMDDYY(result.group(1)), 'decided': dateToMMDDYY(result.group(2))}

    # No match - report an error.
    assert False

# A utility function that, given a list of lines from the opinion, converts that set of lines
# into a string.  This makes several unrealistic assumptions while doing the conversion, so it
# should not be trusted to give back valid English sentences.  However, it will make a best
# effort to do so.
#
# The main conversions being done here are as follows.  First, if a line ends in a dash, then
# the dash is not concatenated onto the end of the string, as it's assumed that we're looking
# at something that was split up for aesthetic reasons.  Otherwise, we append a space to prevent
# the lines from bleeding together.
def linesToString(lines):
    result = ""

    # For each line, process that line according to the above description.
    for line in lines:
        if line[-1] == '-':
            result += line[0:-1]
        else:
            result += line + ' '

    return result

# Now, we're going to try to find how the justices voted on the decision.  This information is
# (empirically) always the very last text on the syllabus for the case, and always starts with
# something of the form "{name}, [C.]J. delivered ...", though the actual contents of the text
# that follows is not necessarily expressed in a nice format.  It's going to be very difficult
# to get an accurate read on what's happening, so we'll just hand back the raw text.
def getDecision(pages):
    # Keep track of whether we found the start of the block.  This is initially set to False
    # and becomes true when we find the line we're looking for.  When it's true, any line that
    # we encounter is agglomerated onto a string containing the result.
    didFind = False
    result = []

    for page in pages:
        for line in page:
            # Try to see if this line looks like the start of an opinion delivery section by seeing
            # if we can match it to the above pattern.

            ######################################################################################################
            # TODO: This needs to be updated to also handle things of the form "[CHIEF ]JUSTICE {NAME} delivered #
            ######################################################################################################
            if re.match(".*,\s*(C\.\s*)?J\.,\s*delivered", line) != None:
                didFind = True

            # If we've found the line we're looking for, append it to the result.
            if didFind:
                result.append(line);

        # If at the end of this loop we've found what we're looking for, we don't need to cross a
        # page boundary.  The info we want is always at the very end of the summary document.
        if didFind:
            break

    # If we didn't find anything, we're in trouble.
    if not didFind:
        return "(unknown)"

    # Convert the result from a list of lines into a string by gluing everything together
    # intelligibly.
    return linesToString(result)

# Main function: getCaseInformation(url)
#
# Given a URL, hands back an object containing the date argued, date decided, and the text of which
# justices delivered opinions in each direction.  It is assumed that the decision is NOT a per curiam
# decision, since the information handed back here is meaningless in that context.
def getCaseInformation(url):
    try:
        pages = getSupremeCourtOpinionPages(url)

        # Recover whether this is a "per curiam" decision or an opinion.  If it's a per curiam, we should not
        # process it, as the structuring is all wrong.

        assert not isPerCuriamDecision(pages)

        return {'dates': getCaseDates(pages), 'decision': getDecision(pages)}
    except lxml.etree.XMLSyntaxError:
        print "WARNING: XML syntax error in " + url
        return {'dates': {'argued': '(unknown)', 'decided': '(unknown)'}, 'decision': '(unknown)'};

main()
import scraperwiki
import urllib
import lxml.etree, lxml.html
import lxml
import re
import urllib2
from BeautifulSoup import BeautifulSoup

def main():
    main_url = "http://www.supremecourt.gov/opinions/opinions.aspx"
    main_html = urllib2.urlopen(main_url)
    soup = BeautifulSoup(main_html)
    listdivs = soup.findAll('div', {'class':'dslist2'})
    for listdiv in listdivs:
        years = listdiv.find('ul')
        years_links = years.findAll('li')
        desired_link = years_links[0].find('a')['href']
        processSinglePage("http://www.supremecourt.gov/opinions/" + desired_link)

def processSinglePage(main_url):
    main_html = urllib2.urlopen(main_url)
    soup = BeautifulSoup(main_html)

    maindiv = soup.find('div', {'id':'maincontentbox'})
    sc_table = maindiv.find('table')
    sc_rows = sc_table.findAll('tr')

    justice_defs = get_justice_defs() # mappings of abbreviations to names

    for sc_row in sc_rows[1:]:
        cells = sc_row.findAll('td')
        seq_num = cells[0].text
        date_decided = cells[1].text
        docket_number = cells[2].text
        pdf_a = cells[3].find('a')
        pdf_url = ''
        if pdf_a:
            pdf_url = 'http://www.supremecourt.gov/opinions/' + pdf_a['href']
        case_name = pdf_a.text 
        
        justice_abbr = cells[4].text
        principal_justice = ''
        if justice_defs.keys().count(justice_abbr) == 0:
            principal_justice = "No definition found"
            print "WARNING: Cannot find definition for " + justice_abbr
        else:
            principal_justice = justice_defs[justice_abbr]

        # If the case isn't per curiam, scrape the contents of the docket.
        if cells[4].text != 'PC':
            case_info = getCaseInformation(pdf_url)
        # Otherwise, fill in the case_info dictionary with reasonable defaults.
        else:
            case_info = {'dates': {'argued': 'None', 'decided': 'date_decided'}, 'decision': 'None'}

        report_vol = cells[5].text
        case_record = {'sequential_number':seq_num, 'date_decided':date_decided, 'docket_number':docket_number, 
            'case_name':case_name,'principal_justice':principal_justice, 'report_volume':report_vol, 
            'date_argued': case_info['dates']['argued'],
            'decision': case_info['decision']}
        scraperwiki.sqlite.save(['case_name','date_decided','docket_number','case_name','principal_justice',
                                 'report_volume','date_argued','decision'],case_record)
        print case_record

def get_justice_defs():
    definition_urls = ["definitions.aspx", "definitions_a.aspx", "definitions_b.aspx", "definitions_c.aspx", "definitions_d.aspx"]
    justice_defs = {}
    for url in definition_urls:
        definition_url = "http://www.supremecourt.gov/opinions/" + url
        definition_soup = BeautifulSoup(urllib2.urlopen(definition_url)) # TODO check it doesn't fail
        definitions_info = definition_soup.find('div', {'id': 'maincontentbox'}).find('blockquote')
        definitions_txt = definitions_info.__str__()
        justice_abbrs = definitions_info.findAll('b')
        for abbr in justice_abbrs:
            reg_ex = '<b>' + abbr.text + '</b>(.*)<' # ASSUMPTION: no html tags within the justice name
            justice_name = re.search((reg_ex), definitions_txt).group(1).strip()
            abbr_txt = abbr.text[:-1] # won't include the ending colon
            if justice_defs.keys().count(abbr_txt) == 0: # new key
                justice_defs[abbr_txt] = justice_name
            elif justice_defs[abbr_txt] != justice_name: # same abbreviation expands to different justice name. this might be a problem i
                print "WARNING: The principal justice may be wrongly scraped. The abbreviation for their name gets used twice over previous years, breaking an assumption in the parsing code. Sorry :("
    return justice_defs

def textFromNode(node):
    return re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(node)).group(1)

# The main challenge of the code at this point is that if we have a single line of text
# that happens to contain nouns in TITLE CASE, the line is split into multiple different
# pieces of text that don't all exist at the same height.  Our idea will therefore be to
# reassemble these fragments into full pieces of text in order to reduce the complexity
# of finding importance pieces of text.
#
# We will make several assumptions in the course of this document processing which are not
# guaranteed to be valid, but which seem to be an artifact of the PDFs.  I'm basing these
# assumptions on a quick inspection of a few PDFs that I've scraped this way.
#
# The first assumption is that if we need to assemble two or more pieces of text into one
# line, that all of the entries on that line will be within some fixed number of pixels
# of one another.  Consider, for example, this snippet of the generated XML:
#
#    <text top="460" left="156" width="296" height="13" font="4">trial counsel to adopt a family-sympathy mitigation de­</text>
#    <text top="473" left="156" width="304" height="13" font="4">fense.  <i>Post</i>, at 27.  She cites no evidence, however, that </text>
#    <text top="487" left="156" width="304" height="13" font="4">such an approach would have been inconsistent with the </text>
#    <text top="500" left="156" width="300" height="13" font="4">standard of professional competence in capital cases that</text>
#    <text top="513" left="156" width="305" height="13" font="4">prevailed in Los Angeles in 1984.  Indeed, she does not </text>
#    <text top="526" left="156" width="303" height="13" font="4">contest that, at the time, the defense bar in California had </text>
#    <text top="540" left="156" width="305" height="13" font="4">been using that strategy.  See <i>supra</i>, at 19; <i>post</i>, at 28, </text>
#    <text top="553" left="156" width="42" height="13" font="4">n. 21.  J</text>
#    <text top="555" left="198" width="38" height="11" font="0">USTICE </text>
#    <text top="553" left="237" width="7" height="13" font="4">S</text>
#    <text top="555" left="244" width="55" height="11" font="0">OTOMAYOR</text>
#    <text top="553" left="299" width="161" height="13" font="4"> relies heavily on <i>Wiggins</i>, but </text>
#    <text top="568" left="156" width="57" height="11" font="0">—————— </text>
#    <text top="582" left="165" width="7" height="7" font="7">17</text>
#
# Notice that the fragments for JUSTIC SOTOMAYOR all have tops that are within a few pixels of
# one another.
#
# This algorithm works by looking for consecutive blocks of text that can be aggredated together.
# Whenever the next piece of text is found, if its top is not within a set window of pixels
# from that last text shard, we assume it's part of a new line.  Otherwise, it will get globbed
# together with the previous piece of text.

kMaxLineDelta = 2 # Maximum permissible change while staying on the same line.

def getSupremeCourtOpinionPages(pdfurl):   
    # Grab the raw PDF data.
    pdfdata = urllib.urlopen(pdfurl).read()
    
    # Convert it to an XML document.
    pdfxml = scraperwiki.pdftoxml(pdfdata)

    # Parse that XML into an XML document tree.
    root = lxml.etree.fromstring(pdfxml)

    # Scan across the pages, building up each into a list of lines.
    pages = []

    for page in root:
        # Verify that the entry we're looking at is indeed a page.
        assert page.tag == 'page'
            
        # Keep track of the piece of text we've accumulated so far, along with its last position.
        # Initially, this is the empty string at a negative offset, which I presume is not going
        # to exist in a PDF document.
        #
        # In particular, I'm going to set the last Y coordinate to a value so that the difference
        # between that Y coordinate and any Y coordinate we find is at least kMaxLineDelta, which
        # forces a new line.
        lastY = -(kMaxLineDelta + 1)
        text = ""
        
        # Keep track of the lines of text from this page.
        lines = []
        
        # Scan over the page contents, reading lines of text from it.
        for v in page:
            # If this is a text node, we need to extract the text contents from it.
            if v.tag == 'text':
                # See whether this is a continuation of the previous line or the start of a brand-
                # new line.
                yCoord = int(v.attrib["top"])
                
                # If this is a new line, record what we have so far.
                if abs(yCoord - lastY) > kMaxLineDelta:
                    # If there's text at all, append it.  There won't be text in some odd cases
                    # where the text is blank, or at the start of this loop.
                    if text != "":
                        lines.append(text)
                        
                    # Clear the accumulated text.
                    text = ""

                # Append to the accumulated text the text from this fragment.  We also strip leading
                # and trailing whitespace to make it easier to do exact matches on the text.
                text += textFromNode(v).strip()

                # Record where this text occurs.
                lastY = yCoord            

            # Otherwise, we assume it's a font specification.  If this is incorrect, abort execution
            # with an error.
            else:
                assert v.tag == 'fontspec'

        # At the very end, if we have any text accumulated, add it to the list of lines.
        if text != "":
            lines.append(text)

        # Finally, record these lines as being part of the page.
        pages.append(lines)

    return pages

# Detects whether an opinion is a Per Curiam decision or a regular opinion.  This current implementation
# is a Gross Awful Hack that works by noticing that on the first page, Per Curium decisions have the header
# "Per Curiam" on the second line, whereas regular decisions have the header "Syllabus."  I believe that
# this works correctly, but I'm not at all proud of it.  Please feel free to fix this if need be.
def isPerCuriamDecision(pages):
    # Confirm that the pages aren't empty.
    assert len(pages) > 0

    # The first page should have at least two lines, the second of which has the text we want.
    assert len(pages[0]) >= 2

    # We should be seeing either Per Curiam or Syllabus here.
    assert pages[0][1] == "Per Curiam" or pages[0][1] == "Syllabus"

    # Hand back whether this is Per Curiam.
    return pages[0][1] == "Per Curiam"

# A utility function to pad a number to two digits by prepending a zero if necessary.
def padNumber(numberAsString):
    if len(numberAsString) == 1:
        return '0' + numberAsString
    else:
        return numberAsString

# A utility function to convert from the {Month} {Day}, {YYYY} format to the simpler MM/DD/YY format
# used elsewhere in the code.
def dateToMMDDYY(date):
    # Use a regular expression to tease apart the date.
    regResult = re.match('(.*?) (\d*), \d\d(\d\d)', date)
    result = ""

    # Convert the month to a number.
    prettyMonth = regResult.group(1)
    if prettyMonth == "January":
        result += "1"
    elif prettyMonth == "February":
        result += "2"
    elif prettyMonth == "March":
        result += "3"
    elif prettyMonth == "April":
        result += "4"
    elif prettyMonth == "May":
        result += "5"
    elif prettyMonth == "June":
        result += "6"
    elif prettyMonth == "July":
        result += "7"
    elif prettyMonth == "August":
        result += "8"
    elif prettyMonth == "September":
        result += "9"
    elif prettyMonth == "October":
        result += "10"
    elif prettyMonth == "November":
        result += "11"
    elif prettyMonth == "December":
        result += "12"
    else:
        assert False

    # Append the day and the year.
    result += "/" + padNumber(regResult.group(2)) + "/" + padNumber(regResult.group(3))
    return result

# Recovers the "date argued" and "date decided" information about a case.  This information should
# be on the very first page of the case description on its own line.
def getCaseDates(pages):
    # Confirm there's at least one page.
    assert len(pages) > 0

    # Scan across all the lines until we find one that matches the appropriate pattern.
    for line in pages[0]:
        # Look for the match against the pattern here, which finds the "Argued" and "Decided" dates.
        result = re.match(".*Argued\s*(.*)&#\d*;Decided\s*(.*)", line)

        # If we didn't match anything, skip this entry.
        if result == None:
            continue

        # Otherwise, package the result into a nice object and hand it back.
        return {'argued': dateToMMDDYY(result.group(1)), 'decided': dateToMMDDYY(result.group(2))}

    # No match - report an error.
    assert False

# A utility function that, given a list of lines from the opinion, converts that set of lines
# into a string.  This makes several unrealistic assumptions while doing the conversion, so it
# should not be trusted to give back valid English sentences.  However, it will make a best
# effort to do so.
#
# The main conversions being done here are as follows.  First, if a line ends in a dash, then
# the dash is not concatenated onto the end of the string, as it's assumed that we're looking
# at something that was split up for aesthetic reasons.  Otherwise, we append a space to prevent
# the lines from bleeding together.
def linesToString(lines):
    result = ""

    # For each line, process that line according to the above description.
    for line in lines:
        if line[-1] == '-':
            result += line[0:-1]
        else:
            result += line + ' '

    return result

# Now, we're going to try to find how the justices voted on the decision.  This information is
# (empirically) always the very last text on the syllabus for the case, and always starts with
# something of the form "{name}, [C.]J. delivered ...", though the actual contents of the text
# that follows is not necessarily expressed in a nice format.  It's going to be very difficult
# to get an accurate read on what's happening, so we'll just hand back the raw text.
def getDecision(pages):
    # Keep track of whether we found the start of the block.  This is initially set to False
    # and becomes true when we find the line we're looking for.  When it's true, any line that
    # we encounter is agglomerated onto a string containing the result.
    didFind = False
    result = []

    for page in pages:
        for line in page:
            # Try to see if this line looks like the start of an opinion delivery section by seeing
            # if we can match it to the above pattern.

            ######################################################################################################
            # TODO: This needs to be updated to also handle things of the form "[CHIEF ]JUSTICE {NAME} delivered #
            ######################################################################################################
            if re.match(".*,\s*(C\.\s*)?J\.,\s*delivered", line) != None:
                didFind = True

            # If we've found the line we're looking for, append it to the result.
            if didFind:
                result.append(line);

        # If at the end of this loop we've found what we're looking for, we don't need to cross a
        # page boundary.  The info we want is always at the very end of the summary document.
        if didFind:
            break

    # If we didn't find anything, we're in trouble.
    if not didFind:
        return "(unknown)"

    # Convert the result from a list of lines into a string by gluing everything together
    # intelligibly.
    return linesToString(result)

# Main function: getCaseInformation(url)
#
# Given a URL, hands back an object containing the date argued, date decided, and the text of which
# justices delivered opinions in each direction.  It is assumed that the decision is NOT a per curiam
# decision, since the information handed back here is meaningless in that context.
def getCaseInformation(url):
    try:
        pages = getSupremeCourtOpinionPages(url)

        # Recover whether this is a "per curiam" decision or an opinion.  If it's a per curiam, we should not
        # process it, as the structuring is all wrong.

        assert not isPerCuriamDecision(pages)

        return {'dates': getCaseDates(pages), 'decision': getDecision(pages)}
    except lxml.etree.XMLSyntaxError:
        print "WARNING: XML syntax error in " + url
        return {'dates': {'argued': '(unknown)', 'decided': '(unknown)'}, 'decision': '(unknown)'};

main()
