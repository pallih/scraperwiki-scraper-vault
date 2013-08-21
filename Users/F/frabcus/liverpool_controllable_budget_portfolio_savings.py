###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
import lxml.etree, lxml.html
import sys
import re
import collections

pdfurl = "http://councillors.liverpool.gov.uk/mgConvert2PDF.aspx?ID=78929"
pdfdata = scraperwiki.scrape(pdfurl)
pdfxml = scraperwiki.pdftoxml(pdfdata)
print pdfxml
root = lxml.etree.fromstring(pdfxml)

# Counts how many times there is a text item starting at
# each left position. Takes the expected_number most popular
# of those and calls them the columns. Asserts that other left
# positions are rarer. Returns an array of the left positions
# of the columns.
def find_pdf_column_lefts(page, expected_number):
    leftcount = collections.defaultdict(int)
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        left = int(v.attrib.get('left'))
        leftcount[left] += 1
    print leftcount
    lefts = leftcount.keys()
    lefts.sort( lambda a,b: cmp(leftcount[b],leftcount[a]) )
    # find the first three columns (as that is what the table has inside this particular PDF)
    columns = lefts[0:expected_number]
    lefts = lefts[expected_number:]
    #for left in lefts:
    #    # make sure the other columns are tiny
    #    assert leftcount[left] < 4
    columns.sort()
    return columns

# Make an array of arrays of the cells. It
# is assumed that text between two columns that
# is at other left positions belongs with the first
# column. Pass in an array of left indices of starts
# of columns - made using find_pdf_column_lefts
def get_content_of_columns(page, columns):
    rows = []
    current_row = []
    current_cell = ""
    current_cell_top = None
    last_left = None
    for v in page:
        if v.tag == 'fontspec':
            continue

        assert v.tag == 'text'
        text = v.text.strip()
        text = re.sub("\s+", " ", text)
        top = int(v.attrib.get('top'))
        left = int(v.attrib.get('left'))
        width = int(v.attrib.get('width'))
        height = int(v.attrib.get('height'))
    
        if left in columns and left != last_left:
            if current_cell != "":
                current_row.append(current_cell)
                current_cell = ""
            if left == columns[0]:
                if current_row != []:
                    rows.append((current_row, current_cell_top))
                    current_row = []

        if current_cell == "":
            current_cell_top = top
        if current_cell != "":
            current_cell += " "
        current_cell += text
        last_left = left

    if current_cell != "":
        current_row.append(current_cell)
    if current_row != []:
        rows.append((current_row, current_cell_top))
    return rows

# Loop through each page of the PDF
portfolio = None
nos = {}
for index, page in enumerate(root):
    page_number = int(page.attrib.get('number'))
    print "Page: ", page_number

    # Extract stuff with height 11, which is body of page
    page_height_11 = [] 
    page_rest = []
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        t = v.text.strip()
        if t == '':
            continue
        if int(v.attrib.get('height')) == 11:
            # ignore some parts of headings that *are* height 11
            if not re.match('^.000s$', t):
                #print t
                page_height_11.append(v)
        else:
            page_rest.append(v)

    # ... check what is left in expected things like headings
    headings = []
    for v in page_rest:
        t = v.text.strip()
        # ignore headings we know about
        if t in ['No.', 'Proposal / Option', '2011/12', '2012/13', 'BUDGET OPTIONS - APPENDIX 1']:
            continue
        # ignore page numbers
        if re.match('^Page \d+$', t):
            continue
        # check what we have left is an all caps category heading
        assert re.match('^[A-Z&/, 0-9-]+$', t), t
        headings.append(v)
    # create index to headings so can work out which heading we were under
    # (we couldn't do this by interleaving as the headings are scattered through
    # the page)
    headings.sort( lambda a,b: cmp(int(a.attrib.get('top')),int(b.attrib.get('top'))) )
    for heading in headings:
           print "portfolio heading:", heading.text, heading.attrib.get('top')        

    # use the height 11 entries
    page = page_height_11

    # Work out where the columns are
    columns = find_pdf_column_lefts(page, 4)
    # ... but take just first two
    print "Column starts:", columns
    columns = columns[0:2]

    # And convert into a table
    rows = get_content_of_columns(page, columns)

    # Final parsing
    for row, row_top in rows:        
        # patches, should be in another system...

        # has a heading for several that messes things up
        m = re.match("^(C3[abcde]) (.*)$", row[0])
        if m:
            row = list(m.groups())
            row[1] = "Children's Centres & Extended Schools " + row[1]
        # ... and clear out where the heading did end up
        if row[0] == "C12":
            assert len(row) == 3
            assert row[2] == "Children's Centres & Extended Schools"
            row.pop()

        # put together some lines that columnated up wrong, e.g.
        # ['LL1', 'Licensing - Increased income 233 294 None.']
        splitat = None
        if len(row) == 2:
            digits = re.findall("[-,\d]+ [-,\d]+", row[1])
            if len(digits) == 1:
                splitat = digits[0]
        if row[0] == 'ASC5':
            splitat = "100 100"
        if row[0] == 'ASC7':
            splitat = "320 320"
        if splitat:
            print "splitting", row, splitat
            a,b = re.split(' ' + splitat + '(?: |$)', row[1])
            row[1] = a.strip()
            row.append(splitat + ' ' + b.strip())

        print row_top, row
        assert len(row) == 3, row

        data = {}
        data['no'] = row[0]
        data['proposal'] = row[1]

        rest = row[2].strip()
        rest_bits = re.match('([\d,-]+) ([\d,-]+)( .*|$)', rest).groups()
        n1 = rest_bits[0].replace(",", "")
        n2 = rest_bits[1].replace(",", "")
        if n1 == '-':
            n1 = '0'
        if n2 == '-':
            n2 = '0'
        data['pounds_saved_2011_2012'] = int(n1) * 1000
        data['pounds_saved_2012_2013'] = int(n2) * 1000
        data['description'] = rest_bits[2].strip()

        # find out which heading it is
        # (or if none on this page it uses the last one from last page)
        for heading in headings:
            if int(heading.attrib.get('top')) > int(row_top):
                break
            portfolio = heading.text
        assert portfolio != None
        data['portfolio'] = portfolio

        assert data['no'] not in nos
        nos[data['no']] = 1
        scraperwiki.datastore.save(['no'], data)
    

    # sys.exit() # only do one page

