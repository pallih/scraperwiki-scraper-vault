import scraperwiki
import urllib2
import lxml.etree
import re
from datetime import date

years = range(date.today().year, 2012, -1) # Races go back to 1999 but no need to update the old results
races = ["a", "b", "c", "d"]
col_names_k1 = ['POSN', 'NO', 'CREW NAME', 'CLUB', 'TIME']
col_names_k2 = ['POSN', 'NO', 'CREW NAMES', 'CLUB', 'TIME']

# Datastore variables
batch_size=100
data_verbose = 0
table_names = { 'results': 'results' }
unique_keys = { 'results': ['race', 'names', 'club'] }
#unique_keys = { 'results': ['race', 'boat_number'] }
data = { 'results': [] }

def get_pdf_url(year, race):
    return "http://www.watersideseries.org.uk/results/%sres%s.pdf" % (year, race)

def get_pdf_text(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append(get_pdf_text(lel))
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def add_line(items, lines):
    text = "".join(items).replace(u'\xa0', u' ').strip()
    if (len(text.strip()) > 0 and text.find('Newbury Canoe Club') != 0 and text.find('www.watersideseries.org.uk') == -1 and text.find('Page') != 0):
        lines.append([i.replace("\r", "").replace("\n", "").replace('&nbsp;', ' ').replace(u'\xa0', u' ') for i in items])

def get_header_positions(rowtext, header_names):
    return [ (rowtext.find(hdr) + len(hdr) - 1) for hdr in header_names ]

def get_col_values(rowtext, header_names, header_positions):
    col_values = []
    if len(header_names) != len(header_positions):
        raise Exception('Number of header names and positions must match')
    stop_pos = len(rowtext)
    for i in range(len(header_names)-1, -1, -1):
        # Get start position
        header_start = header_positions[i] + 1 - len(header_names[i])
        for j in range(header_positions[i], -1, -1):
            if (j <= header_start and rowtext[j] == ' ') or j == 0:
                col_values.append(rowtext[j:stop_pos].strip())
                stop_pos = j
                break
    col_values.reverse()
    return col_values

def is_class_heading(line):
    linec = re.sub(r'RACE[A-D]-', '', line.upper().replace(' ', ''), re.IGNORECASE) # Spaces removed
    return linec.startswith('K1') or linec.startswith('K2') or linec.startswith('CANADIAN') or linec.startswith('JUNIOR') or linec.startswith('RAFT') or linec.startswith('RELAY')

def is_time(timestr):
    return re.match(r'\d+:\d+:\d+$', timestr) is not None

def is_finish_time(timestr):
    return re.match(r'\d+:\d+:\d+|retired|disqualified$', timestr, re.IGNORECASE) is not None

def is_boat_number(numstr):
    return re.match(r'\d+$', numstr) is not None

def is_position(numstr):
    return re.match(r'\d+=?$', numstr) is not None

def fix_row_data(input):
    #print input
    row = []
    # Strip empty items
    for i in input:
        if i.strip() != '':
            row.append(i.strip())
    # Split position if combined with subsequent fields
    m = re.match(r'(\d+=?) +(.+)$', row[0])
    if m is not None:
        row[0:1] = [m.group(1), m.group(2)]
    # Split boat number if combined with subsequent fields
    m = re.match(r'(\d+) +(.*)$', row[1])
    if m is not None:
        row[1:2] = [m.group(1), m.group(2)]
    # Add empty position value if missing
    if row[1] != '' and not is_boat_number(row[1]):
        row[0:1] = ['', row[0]]
    # Add empty boat number if missing
    if row[1] != '' and not is_boat_number(row[1]):
        row[1:2] = ['', row[1]]
    # Strip notes from finish time
    notepos = row[len(row)-1].find('*')
    if notepos > 0:
        row[len(row)-1] = row[len(row)-1][:notepos].strip()
    # Strip parenthesis from finish time
    if re.search(r'\(\d+:\d+:\d+\)', row[len(row)-1]):
        row[len(row)-1] = row[len(row)-1].replace(')', '').replace('(', '')
    # No finish time, should not have a position
    if not re.match(r'\d+:\d+:\d+', row[len(row)-1]) and row[0] != '':
        row[0:1] = ["", row[0]]
    # Split time value if it contains a space
    if row[len(row)-1].find(" ") > 0:
        row[len(row)-1:len(row)] = row[len(row)-1].rsplit(' ', 1)
    # Trim excess empty elements on the start and end (now done up-front)
    #if len(row) > 5 and row[len(row)-1].strip() == '':
    #    del row[len(row)-1:len(row)]
    if len(row) > 5 and row[0].strip() == '' and re.match(r'\d+$', row[2]) is not None:
        del row[0:1]
    # Time may be joined to club
    time = row[len(row)-1].strip()
    if time == '' or not is_finish_time(time):
        clubandtime = "".join(row[len(row)-2:len(row)])
        m = re.search(r'\d+:\d+:\d+|retired|disqualified$', clubandtime, re.IGNORECASE)
        if m is not None:
            row[len(row)-1] = m.group()
            row[len(row)-2] = clubandtime.replace(m.group(), '').strip()
    # Merge names(s) and club, then separate out again
    row = fix_names_clubs(row)
    
    return row

def fix_names_clubs(row):
    if len(row) > 3:
        namesandclubs = " ".join(row[2:len(row)-1]).strip()
        if (namesandclubs == ''):
            row[2:len(row)-1] = ['', '', '']
            return row
        else:
            #print namesandclubs.replace(' ', '.')
            # Two names and club(s)
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+(?: \(\w+\))? +)? ?[JM]? ?& +[\w?\.-]+ [\w?\.'-]+(?: \(\w+\))? ?[JM]?) +([\w /+?\.'&-]+$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)? *& +[\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?) +([\w /+?\.'&-]+)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), match.group(2)]
                #print [match.group(1), match.group(2)]
                return row
            # Two names, no club
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+(?: \(\w+\))? +)? ?[JM]? ?& +[\w?\.-]+(?: [\w?\.'-]+)?(?: \(\w+\))? ?[JM]?$)", namesandclubs)
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+)(?: \(?[JM]\)?)? *& +[\w?\.-]+(?: [\w?\.'-]+)?$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)? *& +[\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)?)", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), '']
                return row
            # Single name and club
            #match = re.match(r"([\w?\.'-]+ +[\w?\.'-]+(?: \(\w+\))? ?[JM]?) +([\w /+?\.'&-]+$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?) +([\w /+?\.'&-]+)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), match.group(2)]
                return row
            # Single name, no club
            #match = re.match(r"([\w?\.'-]+ +[\w?\.'-]+(?: \(\w+\))? ?[JM]?$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), '']
                return row
    elif len(row) == 3 and (row[0] == '' or is_position(row[0])) and is_boat_number(row[1]) and is_finish_time(row[2]):
        row[2:3] = ['', '', row[2]] # Insert blanks for name and club which are obviously missing
    return row

def save_data(result=None, force=False):
    global data
    if result is not None:
        data['results'].append(result)
    if len(data['results']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=unique_keys['results'], data=data['results'], table_name=table_names['results'], verbose=data_verbose)
        data['results'] = []

def save_class_data(raceid, classname, results):
    #print classname, results
    if classname is None or classname == '':
        raise Exception('No class name found, required')
    # remove equals symbol from position
    if results[0].endswith('='):
        results[0] = results[0][:len(results[0])-1]
    save_data(result={'race': raceid, 'race_class': classname, 'position': int(results[0]) if results[0] != '' else None, 'boat_number': results[1], 'names': results[2], 'club': results[3], 'time': results[4]})

def scrape_race(year, race):
    raceid = "%s%s" % (year, race)
    url = get_pdf_url(year, race)
    try:
        pdfdata = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        if e.code == 404 or e.code == 300: # Web server seems to return HTTP Error 300: Multiple Choices when a file is missing!
            print 'WARNING: Missing file for race %s (%s)' % (raceid, url)
            return
        else:
            raise e
    #print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 5000 characters are: ", xmldata[:5000]
    #print "XML: ", xmldata
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    lines = []
    results = []
    lasty = 0
    lastx = 0
    race_class = None
    
    if len(pages) > 1: # Files with only one page indicate the race was cancelled, so skip these
        for page in pages:
            linetext = []
            for el in list(page):
                if el.tag == "text":
                    if lasty == int(el.attrib.get("top")):
                        linetext.append(get_pdf_text(el))
                    else:
                        add_line(linetext, lines)
                        linetext = [get_pdf_text(el)]
                    lastx = int(el.attrib.get("left"))
                    lasty = int(el.attrib.get("top"))
            add_line(linetext, lines)
    else:
        print "File has less than 2 pages, Skipping"
        return
    
    last_line = None
    col_positions = None
    col_names = None
    last_pos = None
    in_results = False

    for line in lines:
        #print line
        completeline = " ".join(line)
        if (completeline.startswith('POS')): # New race
            compressednames = completeline.strip().replace(" ", "").replace("&", "")
            if "".join(col_names_k1).replace(" ", "") == compressednames:
                col_names = col_names_k1
                col_positions = get_header_positions(completeline, col_names)
            elif "".join(col_names_k2).replace(" ", "") == compressednames:
                col_names = col_names_k2
                col_positions = get_header_positions(completeline, col_names)
            else:
                raise Exception('Bad columns %s' % re.sub(r' +', ' ', completeline.strip()))
            if (is_class_heading(last_line)):
                race_class = re.sub(r'Race [A-D] -? ?', '', re.sub(r'[^\w/]+', ' ', last_line.strip()), re.IGNORECASE)
                in_results = True
                #print race_class
            else:
                print last_line.strip() # Unicode characters in the exception message cause SW to thrown an exception itself!
                raise Exception('Bad race class')
            #print col_positions
        elif (completeline.find('Waterside Series') == 0 or completeline.find('Watersides') == 0): # Skip titles
            pass
        elif (re.search(r'\d+ +Starters', completeline.strip()) is not None):
            in_results = False
        elif (re.search(r'\d+ +Finishers', completeline.strip()) is not None):
            in_results = False
        elif re.search(r'\d+', completeline) is None: # If no numbers at all in the line assume it is of no consequence
            pass
        elif completeline.strip().find("**") == 0: # Notes, e.g. penalties applied are marked with asterisks
            pass
        elif (is_class_heading(completeline)): # This separate item is needed in addition to the logic under 'POS' above as some old docs have no column headings
            race_class = re.sub(r'[^\w/]+', ' ', completeline.strip())
            in_results = True
            #print race_class
        elif in_results == True:
            if len(line) == 1:
                if len(line[0].strip()) > 20 and race_class is not None: # Assume this is row data
                    if col_names is not None:
                        values = fix_row_data(get_col_values(line[0], col_names, col_positions))
                        if len(values) == 5:
                            if (len(values) != len(col_names)):
                                raise Exception('Incorrect column length for row: %s' % (line[0]))
                            if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                                values[0] = last_pos
                            last_pos = values[0]
                            save_class_data(raceid, race_class, values)
                        else:
                            raise Exception('Incorrect data length for row: %s, original %s' % (values, line))
                    else: # 2003c has no column names
                        posmatch = re.search(r"^\d+", line[0].strip())
                        timematch = re.search(r"\d+:\d+:\d+|retired|disqualified$", line[0].strip())
                        if (posmatch and timematch):
                            values = fix_row_data([posmatch.group(), '', re.sub(r"^\d+", '', re.sub(r"\d+:\d+:\d+|retired|disqualified$", '', line[0].strip())).strip(), timematch.group()])
                            if len(values) != 5:
                                raise Exception('Bad data length: %s' % (values))
                            if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                                values[0] = last_pos
                            last_pos = values[0]
                            save_class_data(raceid, race_class, values)
                        else:
                            raise Exception('No column names when parsing row: %s' % (line[0]))
                #last_line = line[0]
            # Handle array being larger than 1
            elif len(line) == 5:
                values = fix_row_data(line)
                if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                    values[0] = last_pos
                last_pos = values[0]
                save_class_data(raceid, race_class, values)
            else:
                if not is_class_heading(line[0]) and race_class is not None:
                    fixed_row = fix_row_data([ col.strip() for col in line ])
                    if len(fixed_row) != 5:
                        print "!!! Bad row length: %s - original %s" % (fixed_row, [ col.strip() for col in line ])

        if len(completeline.strip()) > 0 and (not completeline.strip().startswith('Page')) and (not completeline.strip().startswith('Waterside')):
            last_line = completeline

for year in years:
    for race in races:
        print "Scraping %s%s" % (year, race)
        scrape_race(year, race)

save_data(force=True)
import scraperwiki
import urllib2
import lxml.etree
import re
from datetime import date

years = range(date.today().year, 2012, -1) # Races go back to 1999 but no need to update the old results
races = ["a", "b", "c", "d"]
col_names_k1 = ['POSN', 'NO', 'CREW NAME', 'CLUB', 'TIME']
col_names_k2 = ['POSN', 'NO', 'CREW NAMES', 'CLUB', 'TIME']

# Datastore variables
batch_size=100
data_verbose = 0
table_names = { 'results': 'results' }
unique_keys = { 'results': ['race', 'names', 'club'] }
#unique_keys = { 'results': ['race', 'boat_number'] }
data = { 'results': [] }

def get_pdf_url(year, race):
    return "http://www.watersideseries.org.uk/results/%sres%s.pdf" % (year, race)

def get_pdf_text(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append(get_pdf_text(lel))
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def add_line(items, lines):
    text = "".join(items).replace(u'\xa0', u' ').strip()
    if (len(text.strip()) > 0 and text.find('Newbury Canoe Club') != 0 and text.find('www.watersideseries.org.uk') == -1 and text.find('Page') != 0):
        lines.append([i.replace("\r", "").replace("\n", "").replace('&nbsp;', ' ').replace(u'\xa0', u' ') for i in items])

def get_header_positions(rowtext, header_names):
    return [ (rowtext.find(hdr) + len(hdr) - 1) for hdr in header_names ]

def get_col_values(rowtext, header_names, header_positions):
    col_values = []
    if len(header_names) != len(header_positions):
        raise Exception('Number of header names and positions must match')
    stop_pos = len(rowtext)
    for i in range(len(header_names)-1, -1, -1):
        # Get start position
        header_start = header_positions[i] + 1 - len(header_names[i])
        for j in range(header_positions[i], -1, -1):
            if (j <= header_start and rowtext[j] == ' ') or j == 0:
                col_values.append(rowtext[j:stop_pos].strip())
                stop_pos = j
                break
    col_values.reverse()
    return col_values

def is_class_heading(line):
    linec = re.sub(r'RACE[A-D]-', '', line.upper().replace(' ', ''), re.IGNORECASE) # Spaces removed
    return linec.startswith('K1') or linec.startswith('K2') or linec.startswith('CANADIAN') or linec.startswith('JUNIOR') or linec.startswith('RAFT') or linec.startswith('RELAY')

def is_time(timestr):
    return re.match(r'\d+:\d+:\d+$', timestr) is not None

def is_finish_time(timestr):
    return re.match(r'\d+:\d+:\d+|retired|disqualified$', timestr, re.IGNORECASE) is not None

def is_boat_number(numstr):
    return re.match(r'\d+$', numstr) is not None

def is_position(numstr):
    return re.match(r'\d+=?$', numstr) is not None

def fix_row_data(input):
    #print input
    row = []
    # Strip empty items
    for i in input:
        if i.strip() != '':
            row.append(i.strip())
    # Split position if combined with subsequent fields
    m = re.match(r'(\d+=?) +(.+)$', row[0])
    if m is not None:
        row[0:1] = [m.group(1), m.group(2)]
    # Split boat number if combined with subsequent fields
    m = re.match(r'(\d+) +(.*)$', row[1])
    if m is not None:
        row[1:2] = [m.group(1), m.group(2)]
    # Add empty position value if missing
    if row[1] != '' and not is_boat_number(row[1]):
        row[0:1] = ['', row[0]]
    # Add empty boat number if missing
    if row[1] != '' and not is_boat_number(row[1]):
        row[1:2] = ['', row[1]]
    # Strip notes from finish time
    notepos = row[len(row)-1].find('*')
    if notepos > 0:
        row[len(row)-1] = row[len(row)-1][:notepos].strip()
    # Strip parenthesis from finish time
    if re.search(r'\(\d+:\d+:\d+\)', row[len(row)-1]):
        row[len(row)-1] = row[len(row)-1].replace(')', '').replace('(', '')
    # No finish time, should not have a position
    if not re.match(r'\d+:\d+:\d+', row[len(row)-1]) and row[0] != '':
        row[0:1] = ["", row[0]]
    # Split time value if it contains a space
    if row[len(row)-1].find(" ") > 0:
        row[len(row)-1:len(row)] = row[len(row)-1].rsplit(' ', 1)
    # Trim excess empty elements on the start and end (now done up-front)
    #if len(row) > 5 and row[len(row)-1].strip() == '':
    #    del row[len(row)-1:len(row)]
    if len(row) > 5 and row[0].strip() == '' and re.match(r'\d+$', row[2]) is not None:
        del row[0:1]
    # Time may be joined to club
    time = row[len(row)-1].strip()
    if time == '' or not is_finish_time(time):
        clubandtime = "".join(row[len(row)-2:len(row)])
        m = re.search(r'\d+:\d+:\d+|retired|disqualified$', clubandtime, re.IGNORECASE)
        if m is not None:
            row[len(row)-1] = m.group()
            row[len(row)-2] = clubandtime.replace(m.group(), '').strip()
    # Merge names(s) and club, then separate out again
    row = fix_names_clubs(row)
    
    return row

def fix_names_clubs(row):
    if len(row) > 3:
        namesandclubs = " ".join(row[2:len(row)-1]).strip()
        if (namesandclubs == ''):
            row[2:len(row)-1] = ['', '', '']
            return row
        else:
            #print namesandclubs.replace(' ', '.')
            # Two names and club(s)
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+(?: \(\w+\))? +)? ?[JM]? ?& +[\w?\.-]+ [\w?\.'-]+(?: \(\w+\))? ?[JM]?) +([\w /+?\.'&-]+$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)? *& +[\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?) +([\w /+?\.'&-]+)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), match.group(2)]
                #print [match.group(1), match.group(2)]
                return row
            # Two names, no club
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+(?: \(\w+\))? +)? ?[JM]? ?& +[\w?\.-]+(?: [\w?\.'-]+)?(?: \(\w+\))? ?[JM]?$)", namesandclubs)
            #match = re.match(r"([\w?\.'-]+ +(?:[\w?\.'-]+)(?: \(?[JM]\)?)? *& +[\w?\.-]+(?: [\w?\.'-]+)?$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)? *& +[\w?\.'-]+(?: +(?:(?:van|von|de) )?[\w?\.'-]+)?(?: +\(?[JM]\)?)?)", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), '']
                return row
            # Single name and club
            #match = re.match(r"([\w?\.'-]+ +[\w?\.'-]+(?: \(\w+\))? ?[JM]?) +([\w /+?\.'&-]+$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?) +([\w /+?\.'&-]+)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), match.group(2)]
                return row
            # Single name, no club
            #match = re.match(r"([\w?\.'-]+ +[\w?\.'-]+(?: \(\w+\))? ?[JM]?$)", namesandclubs)
            match = re.match(r"([\w?\.'-]+ +(?:(?:van|von|de) )?[\w?\.'-]+(?: +\(?[JM]\)?)?)$", namesandclubs, re.I)
            if match is not None:
                row[2:len(row)-1] = [match.group(1), '']
                return row
    elif len(row) == 3 and (row[0] == '' or is_position(row[0])) and is_boat_number(row[1]) and is_finish_time(row[2]):
        row[2:3] = ['', '', row[2]] # Insert blanks for name and club which are obviously missing
    return row

def save_data(result=None, force=False):
    global data
    if result is not None:
        data['results'].append(result)
    if len(data['results']) >= batch_size or force == True:
        scraperwiki.sqlite.save(unique_keys=unique_keys['results'], data=data['results'], table_name=table_names['results'], verbose=data_verbose)
        data['results'] = []

def save_class_data(raceid, classname, results):
    #print classname, results
    if classname is None or classname == '':
        raise Exception('No class name found, required')
    # remove equals symbol from position
    if results[0].endswith('='):
        results[0] = results[0][:len(results[0])-1]
    save_data(result={'race': raceid, 'race_class': classname, 'position': int(results[0]) if results[0] != '' else None, 'boat_number': results[1], 'names': results[2], 'club': results[3], 'time': results[4]})

def scrape_race(year, race):
    raceid = "%s%s" % (year, race)
    url = get_pdf_url(year, race)
    try:
        pdfdata = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        if e.code == 404 or e.code == 300: # Web server seems to return HTTP Error 300: Multiple Choices when a file is missing!
            print 'WARNING: Missing file for race %s (%s)' % (raceid, url)
            return
        else:
            raise e
    #print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 5000 characters are: ", xmldata[:5000]
    #print "XML: ", xmldata
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    lines = []
    results = []
    lasty = 0
    lastx = 0
    race_class = None
    
    if len(pages) > 1: # Files with only one page indicate the race was cancelled, so skip these
        for page in pages:
            linetext = []
            for el in list(page):
                if el.tag == "text":
                    if lasty == int(el.attrib.get("top")):
                        linetext.append(get_pdf_text(el))
                    else:
                        add_line(linetext, lines)
                        linetext = [get_pdf_text(el)]
                    lastx = int(el.attrib.get("left"))
                    lasty = int(el.attrib.get("top"))
            add_line(linetext, lines)
    else:
        print "File has less than 2 pages, Skipping"
        return
    
    last_line = None
    col_positions = None
    col_names = None
    last_pos = None
    in_results = False

    for line in lines:
        #print line
        completeline = " ".join(line)
        if (completeline.startswith('POS')): # New race
            compressednames = completeline.strip().replace(" ", "").replace("&", "")
            if "".join(col_names_k1).replace(" ", "") == compressednames:
                col_names = col_names_k1
                col_positions = get_header_positions(completeline, col_names)
            elif "".join(col_names_k2).replace(" ", "") == compressednames:
                col_names = col_names_k2
                col_positions = get_header_positions(completeline, col_names)
            else:
                raise Exception('Bad columns %s' % re.sub(r' +', ' ', completeline.strip()))
            if (is_class_heading(last_line)):
                race_class = re.sub(r'Race [A-D] -? ?', '', re.sub(r'[^\w/]+', ' ', last_line.strip()), re.IGNORECASE)
                in_results = True
                #print race_class
            else:
                print last_line.strip() # Unicode characters in the exception message cause SW to thrown an exception itself!
                raise Exception('Bad race class')
            #print col_positions
        elif (completeline.find('Waterside Series') == 0 or completeline.find('Watersides') == 0): # Skip titles
            pass
        elif (re.search(r'\d+ +Starters', completeline.strip()) is not None):
            in_results = False
        elif (re.search(r'\d+ +Finishers', completeline.strip()) is not None):
            in_results = False
        elif re.search(r'\d+', completeline) is None: # If no numbers at all in the line assume it is of no consequence
            pass
        elif completeline.strip().find("**") == 0: # Notes, e.g. penalties applied are marked with asterisks
            pass
        elif (is_class_heading(completeline)): # This separate item is needed in addition to the logic under 'POS' above as some old docs have no column headings
            race_class = re.sub(r'[^\w/]+', ' ', completeline.strip())
            in_results = True
            #print race_class
        elif in_results == True:
            if len(line) == 1:
                if len(line[0].strip()) > 20 and race_class is not None: # Assume this is row data
                    if col_names is not None:
                        values = fix_row_data(get_col_values(line[0], col_names, col_positions))
                        if len(values) == 5:
                            if (len(values) != len(col_names)):
                                raise Exception('Incorrect column length for row: %s' % (line[0]))
                            if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                                values[0] = last_pos
                            last_pos = values[0]
                            save_class_data(raceid, race_class, values)
                        else:
                            raise Exception('Incorrect data length for row: %s, original %s' % (values, line))
                    else: # 2003c has no column names
                        posmatch = re.search(r"^\d+", line[0].strip())
                        timematch = re.search(r"\d+:\d+:\d+|retired|disqualified$", line[0].strip())
                        if (posmatch and timematch):
                            values = fix_row_data([posmatch.group(), '', re.sub(r"^\d+", '', re.sub(r"\d+:\d+:\d+|retired|disqualified$", '', line[0].strip())).strip(), timematch.group()])
                            if len(values) != 5:
                                raise Exception('Bad data length: %s' % (values))
                            if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                                values[0] = last_pos
                            last_pos = values[0]
                            save_class_data(raceid, race_class, values)
                        else:
                            raise Exception('No column names when parsing row: %s' % (line[0]))
                #last_line = line[0]
            # Handle array being larger than 1
            elif len(line) == 5:
                values = fix_row_data(line)
                if len(values[0]) == 0 and last_pos is not None and last_pos.endswith('='):
                    values[0] = last_pos
                last_pos = values[0]
                save_class_data(raceid, race_class, values)
            else:
                if not is_class_heading(line[0]) and race_class is not None:
                    fixed_row = fix_row_data([ col.strip() for col in line ])
                    if len(fixed_row) != 5:
                        print "!!! Bad row length: %s - original %s" % (fixed_row, [ col.strip() for col in line ])

        if len(completeline.strip()) > 0 and (not completeline.strip().startswith('Page')) and (not completeline.strip().startswith('Waterside')):
            last_line = completeline

for year in years:
    for race in races:
        print "Scraping %s%s" % (year, race)
        scrape_race(year, race)

save_data(force=True)
