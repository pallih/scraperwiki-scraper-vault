### Scraper for British Columbia Court Lists.
# This was thrown together rather quickly, so it may exhibit some rather peculiar coding habits...

# See: http://www.ag.gov.bc.ca/courts/court-lists/criminal/index.htm for abbreviations used.

# We scrape PDFs as well as one can based on limited understanding of the actual data. We mostly preserve the newlines from the original PDFs in entries since there is not a simple way to understand whether they are real newlines (as opposed to wrapped text) or not.

# Each Court File Number can have multiple 'Counts'. We store each Count as a separate record. So (Court, File Number, File Appeared on) is not a unique_key, but (Court, File Number, File Appeared on, Count) is. It's then up to the user of the data to arrange records how they like, probably by File Number.

# The PDFs scraped show listings for the last five days (and are updated each day) so this should be run preferably once a day and no less than once every five days.

import re
from lxml import etree
import scraperwiki

# some helper functions
def unmarkup(e): # remove xml markup
    return etree.tostring(e, method = 'text', with_tail = False)
def getattribs(e):
    return int(e.get('left')), int(e.get('top')), int(e.get('font'))
def dicttolist(d):
    t = []
    for key in sorted(d.keys()):
        t.append(d[key])
    return t
def flattendict(d, sep):
    t = ''
    for key in sorted(d.keys()):
        if t.endswith('-'):
            t += d[key]
        else:
            t += sep + d[key]
    return t.strip(sep).strip()
def entry_nonempty(d, entry):
    if d.has_key(entry) and d[entry]:
        return True
    else:
        return False    
def closest(x, points): # return closest number to x in points
    return min( ((i - x)*(i - x), i) for i in points )[1]

def parsearea(page, primary, top, bottom):
    columns = {}
    entries ={}
    entry_rows = []
    for e in page.iter('text'):
        text = unmarkup(e)
        x, y, f = getattribs(e)
        if y > bottom or y < top:
            continue
        if f == 3:
            if columns.has_key(x):
                columns[x][y] = text
            else:
                columns[x] = {y:text}
            if text == primary:
                primary_column = x
    for entry in columns.iterkeys():
        columns[entry] = flattendict(columns[entry], ' ')
    for e in page.iter('text'):
        text = unmarkup(e)
        x, y, f = getattribs(e)
        if y > bottom or y < top:
            continue
        if f == 2 and text != 'No sittings for this location.':
            if closest(x, columns.iterkeys()) == primary_column:
                entry_rows.append(y)
                entries[y] = {}
    if len(entry_rows) == 0:
        return {}
    entry_rows.sort()
    for e in page.iter('text'):
        text = unmarkup(e)
        x, y, f = getattribs(e)
        if y > bottom or y < top:
            continue
        if f == 2 and text != 'No sittings for this location.':
            for i in reversed(entry_rows):
                if i <= y:
                    entry = i
                    break
            col = columns[closest(x,columns.iterkeys())]
            if entries[entry].has_key(col):
                entries[entry][col][y] = text
            else:
                entries[entry][col] = {y:text}
    for entry in entries:
        for col in entries[entry]:
            entries[entry][col] = flattendict(entries[entry][col], '\n')
    return entries

def joinentries(files, cnts):
    output = []
    for row in sorted(cnts.keys()):
        if entry_nonempty(cnts[row], 'Rm'):
            pass # new room
        else:
            cnts[row]['Rm'] = cnts[prev]['Rm']
        if entry_nonempty(cnts[row], 'File Number'): # at top of file
            cnts[row]['Name'] = files[closest(row, files.iterkeys())]['Name']
        else:
            cnts[row]['File Number'] = cnts[prev]['File Number']
            cnts[row]['Name'] = cnts[prev]['Name']
            if entry_nonempty(cnts[prev], 'Bail Proc'):
                cnts[row]['Bail Proc'] = cnts[prev]['Bail Proc']
            if entry_nonempty(cnts[prev], 'I/C'):
                cnts[row]['I/C'] = cnts[prev]['I/C']
        prev = row
        output.append(cnts[row])
    return output

def parsepage(page):
    basicinfo = {'Report Page':page.attrib['number']}  
    title_rows = {}
    type_rows = {}
    appear_rows = {}
    for e in page.iter('text'):
        text = unmarkup(e)
        x, y, f = getattribs(e)
        m = re.search('Report Id:  (.+?) ', text)
        n = re.search('For Files Appearing on (.+)', text)
        if f == 0:
            if text == 'Report Date: ':
                date_row = y
            elif m:
                basicinfo['Report Id'] = m.group(1)
        elif f == 1:
            if text.find('Public Access Completed') != -1:
                type_rows[y] = text
            elif n:
                appear_rows[y] = n.group(1)
            else:
                title_rows[y] = text
    for e in page.iter('text'):
        text = unmarkup(e)
        x, y, f = getattribs(e)
        m = re.search('Report Id:  (.+?) ', text)
        if f == 0 and y == date_row and not m and text != 'Report Date: ':
                basicinfo['Report Date'] = text
                break
    bottom = date_row
    output = []
    type_rows = dicttolist(type_rows)
    appear_rows = dicttolist(appear_rows)
    type_rows.reverse()
    appear_rows.reverse()
    i = 0
    for top in reversed(title_rows.keys()):
        basicinfo['Court'] = title_rows[top]
        basicinfo['List Type'] = type_rows[i]
        basicinfo['File Appeared on'] = appear_rows[i]
        files = parsearea(page, 'File Number', top, bottom)
        cnts = parsearea(page, 'Cnt', top, bottom)
        for entry in cnts:
            cnts[entry].update(basicinfo)
        output.extend(joinentries(files, cnts))
        i += 1
        bottom = top
    return output

def getlistings(url):
    html = scraperwiki.scrape(url)
    for f in re.findall(r"<a href=lists/(.+?\.pdf)>", html):
        print "Fetching " + f
        pdf = scraperwiki.scrape('http://www.ag.gov.bc.ca/courts/court-lists/criminal/lists/' + f)
        print "Scraping " + f
        xml = scraperwiki.pdftoxml(pdf)
        root = etree.XML(xml)
        for page in root:
            print "Saving page " + page.attrib['number']
            records = parsepage(page)
            def stupid_scraperwiki_changed_something_and_broke_my_scraper_and_this_is_a_quick_and_rubbish_fix(record):
                if record.has_key('I/C'):
                    record['IC']=record['I/C']
                    del record['I/C']
            for record in records:
                stupid_scraperwiki_changed_something_and_broke_my_scraper_and_this_is_a_quick_and_rubbish_fix(record)
                scraperwiki.datastore.save(unique_keys=['Court', 'List Type', 'File Number', 'File Appeared on', 'Cnt'], data = record)

def main():
    getlistings('http://www.ag.gov.bc.ca/courts/court-lists/criminal/DACCPindex.html')
    getlistings('http://www.ag.gov.bc.ca/courts/court-lists/criminal/DACCSindex.html')

main()

