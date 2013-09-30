import urllib2
import urllib
import re
import os
import itertools
import pprint
import json
import time
import bz2
import base64
import cPickle
import scraperwiki
import datetime

time.clock()

#http://www.decalage.info/en/python/html

def wiki_api_call(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'TableBot/aidanhs-at-live.co.uk')]
    # Rate limit of 10s per request to be polite
    diff = time.clock()
    if diff < 10:
        time.sleep(10-diff)
    return opener.open(url)

def get_markup(page):
    apibase = "http://en.wikipedia.org/w/index.php?"
    cmd = "title=%s&action=raw" % urllib.quote(page)
    markup = wiki_api_call(apibase + cmd).read()
    return markup

def preprocess(markup):
    """ Preprocessing: Get rid of comments, captions, blank lines """
    markup = re.sub(u"<!--.*?-->","",markup, flags=re.DOTALL)
    markup_linelist = markup.splitlines(False)
    markup_linelist = [l for l in markup_linelist if not l.startswith("|+")]
    markup_linelist = [l for l in markup_linelist if l.strip()]
    markup = os.linesep.join(markup_linelist)
    return markup

def split_tables(markup):
    """ Split the markup into a list of tables """
    # Assume the brakets are well formed, do only basic checking
    markup_linelist = markup.splitlines(False)
    newtable_locations = []
    table_ranges = []
    # Get a list of table start and finish positions
    # Strips out overall table formatting
    for line,i in zip(markup_linelist,range(len(markup_linelist))):
        if line.startswith("{|"):
            newtable_locations.append(i)
        elif line.startswith("|}"):
            table_ranges.append((newtable_locations.pop(),i))
    # Shouldn't have any unmatched brackets
    if newtable_locations:
        raise Exception
    # Only want the top level tables for now
    prev_table = (0,0)
    for table in table_ranges[:]:
        if table[0] < prev_table[0]:
            table_ranges.remove(prev_table)
        prev_table = table
    # Actually get the contents of each row
    tables_list = []
    for table in table_ranges:
        table_markup = os.linesep.join(markup_linelist[table[0]:table[1]])
        tables_list.append(table_markup)
    return tables_list
    
def split_rows(table_markup):
    """ Take the source of a single table and split it into rows """
    table_markup_linelist = table_markup.splitlines(False)
    newrow_locations = []
    # Get a list of row start and finish positions
    for line,i in zip(table_markup_linelist,range(len(table_markup_linelist))):
        if line.startswith("|-"):
            newrow_locations.append(i)
    row_ranges = zip(newrow_locations,newrow_locations[1:])
    # Dont want the row header (i.e. formatting) so modify the line no range
    row_ranges = map(lambda (x,y):(x+1,y), row_ranges)
    # Actually get the contents of each row
    row_list = []
    for row in row_ranges:
        row_markup = os.linesep.join(table_markup_linelist[row[0]:row[1]])
        row_list.append(row_markup)
    return row_list

def split_cells(row_markup):
    """ Take the source of a single row and split it into cells """
    # Allow detection of first line
    cell_list = [os.linesep + row_markup]
    # Split by newlines (we can use os.linesep because we've joined
    # with it before) and flatten
    cell_list = [item.split(os.linesep + "|") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    cell_list = [item.split(os.linesep + "!") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    # Split by || and flatten
    cell_list = [item.split("||") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    # Clean up the cells, no need to flatten
    cell_list = [item.strip() for item in cell_list]
    return cell_list

def write_table(python_table):
    """ Take a python table (list of lists) and write it as a html table """
    yield '<table>\n'
    for python_row in python_table:
        yield '<tr>'
        yield '<td>' + '</td><td>'.join(python_row) + '</td>'
        yield '</tr>\n'
    yield '</table>\n'

def write_html(tables):
    """ Take a list of python tables (list of list of lists) and write it to html output """
    yield '<html><head>\n'
    yield '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
    yield '</head><body>\n'
    for t in tables:
        yield "".join(write_table(t))
    yield '</body></html>'

def markup_to_python(markup):
    """ Extract tables from mediawiki markup and return as a python table (list of list of lists) """
    # Return a list of tables
    # Where each table is a list of rows
    # Where each row is a list of cells
    markup = preprocess(markup)
    tablelist = split_tables(markup)
    tablerowlist = []
    for table in tablelist:
        tablerowlist.append(split_rows(table))
    tablerowcelllist = []
    for table in tablerowlist:
        row_list = []
        for row in table:
            row_list.append(split_cells(row))
        tablerowcelllist.append(row_list)
    return tablerowcelllist

def markup_to_jsonhtml(markup):
    """ Use the mediawiki api to convert markup to html """
    apibase = "http://en.wikipedia.org/w/api.php"
    cmd = "action=parse&format=json&text=" + urllib.quote(markup.encode("utf-8"))
    html = wiki_api_call(apibase, cmd).read()
    with open("example_html_json.txt","wb") as f:
        f.write(html)

def python_to_markup(python_tables):
    """ Convert a list of python tables to wiki markup """
    tables_source = ""
    for table in python_tables:
        tables_source = tables_source + "{|\n"
        rows_source = ""
        for row in table:
            rows_source = rows_source + "|-" + os.linesep
            cells_source = "|"
            for cell in row:
                cells_source = cells_source + cell + "||"
            rows_source = rows_source + cells_source[:-2] + os.linesep
        tables_source = tables_source + rows_source + "|}\n"
    return tables_source

def maintain():
    scraperwiki.sqlite.execute("DROP TABLE table_pages")
    scraperwiki.sqlite.execute("CREATE TABLE table_pages (id TEXT PRIMARY KEY, python_table BLOB, date TEXT)")
#maintain()

page = "Comparison of open source software hosting facilities"
python_table = markup_to_python(get_markup(page))

#print len(base64.b64encode(bz2.compress(buffer(cPickle.dumps(python_table,2))))) #12076
#print len(base64.b64encode(cPickle.dumps(python_table,2)))                       #38404
#print len(cPickle.dumps(python_table,0))                                         #32967
scraperwiki.sqlite.execute("INSERT INTO table_pages values(?,?,?)", (page, cPickle.dumps(python_table,0), str(datetime.date.today())))
#datetime.datetime.strptime(z,"%Y-%m-%d")
scraperwiki.sqlite.commit()


import urllib2
import urllib
import re
import os
import itertools
import pprint
import json
import time
import bz2
import base64
import cPickle
import scraperwiki
import datetime

time.clock()

#http://www.decalage.info/en/python/html

def wiki_api_call(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'TableBot/aidanhs-at-live.co.uk')]
    # Rate limit of 10s per request to be polite
    diff = time.clock()
    if diff < 10:
        time.sleep(10-diff)
    return opener.open(url)

def get_markup(page):
    apibase = "http://en.wikipedia.org/w/index.php?"
    cmd = "title=%s&action=raw" % urllib.quote(page)
    markup = wiki_api_call(apibase + cmd).read()
    return markup

def preprocess(markup):
    """ Preprocessing: Get rid of comments, captions, blank lines """
    markup = re.sub(u"<!--.*?-->","",markup, flags=re.DOTALL)
    markup_linelist = markup.splitlines(False)
    markup_linelist = [l for l in markup_linelist if not l.startswith("|+")]
    markup_linelist = [l for l in markup_linelist if l.strip()]
    markup = os.linesep.join(markup_linelist)
    return markup

def split_tables(markup):
    """ Split the markup into a list of tables """
    # Assume the brakets are well formed, do only basic checking
    markup_linelist = markup.splitlines(False)
    newtable_locations = []
    table_ranges = []
    # Get a list of table start and finish positions
    # Strips out overall table formatting
    for line,i in zip(markup_linelist,range(len(markup_linelist))):
        if line.startswith("{|"):
            newtable_locations.append(i)
        elif line.startswith("|}"):
            table_ranges.append((newtable_locations.pop(),i))
    # Shouldn't have any unmatched brackets
    if newtable_locations:
        raise Exception
    # Only want the top level tables for now
    prev_table = (0,0)
    for table in table_ranges[:]:
        if table[0] < prev_table[0]:
            table_ranges.remove(prev_table)
        prev_table = table
    # Actually get the contents of each row
    tables_list = []
    for table in table_ranges:
        table_markup = os.linesep.join(markup_linelist[table[0]:table[1]])
        tables_list.append(table_markup)
    return tables_list
    
def split_rows(table_markup):
    """ Take the source of a single table and split it into rows """
    table_markup_linelist = table_markup.splitlines(False)
    newrow_locations = []
    # Get a list of row start and finish positions
    for line,i in zip(table_markup_linelist,range(len(table_markup_linelist))):
        if line.startswith("|-"):
            newrow_locations.append(i)
    row_ranges = zip(newrow_locations,newrow_locations[1:])
    # Dont want the row header (i.e. formatting) so modify the line no range
    row_ranges = map(lambda (x,y):(x+1,y), row_ranges)
    # Actually get the contents of each row
    row_list = []
    for row in row_ranges:
        row_markup = os.linesep.join(table_markup_linelist[row[0]:row[1]])
        row_list.append(row_markup)
    return row_list

def split_cells(row_markup):
    """ Take the source of a single row and split it into cells """
    # Allow detection of first line
    cell_list = [os.linesep + row_markup]
    # Split by newlines (we can use os.linesep because we've joined
    # with it before) and flatten
    cell_list = [item.split(os.linesep + "|") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    cell_list = [item.split(os.linesep + "!") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    # Split by || and flatten
    cell_list = [item.split("||") for item in cell_list]
    cell_list = list(itertools.chain.from_iterable(cell_list))
    # Clean up the cells, no need to flatten
    cell_list = [item.strip() for item in cell_list]
    return cell_list

def write_table(python_table):
    """ Take a python table (list of lists) and write it as a html table """
    yield '<table>\n'
    for python_row in python_table:
        yield '<tr>'
        yield '<td>' + '</td><td>'.join(python_row) + '</td>'
        yield '</tr>\n'
    yield '</table>\n'

def write_html(tables):
    """ Take a list of python tables (list of list of lists) and write it to html output """
    yield '<html><head>\n'
    yield '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'
    yield '</head><body>\n'
    for t in tables:
        yield "".join(write_table(t))
    yield '</body></html>'

def markup_to_python(markup):
    """ Extract tables from mediawiki markup and return as a python table (list of list of lists) """
    # Return a list of tables
    # Where each table is a list of rows
    # Where each row is a list of cells
    markup = preprocess(markup)
    tablelist = split_tables(markup)
    tablerowlist = []
    for table in tablelist:
        tablerowlist.append(split_rows(table))
    tablerowcelllist = []
    for table in tablerowlist:
        row_list = []
        for row in table:
            row_list.append(split_cells(row))
        tablerowcelllist.append(row_list)
    return tablerowcelllist

def markup_to_jsonhtml(markup):
    """ Use the mediawiki api to convert markup to html """
    apibase = "http://en.wikipedia.org/w/api.php"
    cmd = "action=parse&format=json&text=" + urllib.quote(markup.encode("utf-8"))
    html = wiki_api_call(apibase, cmd).read()
    with open("example_html_json.txt","wb") as f:
        f.write(html)

def python_to_markup(python_tables):
    """ Convert a list of python tables to wiki markup """
    tables_source = ""
    for table in python_tables:
        tables_source = tables_source + "{|\n"
        rows_source = ""
        for row in table:
            rows_source = rows_source + "|-" + os.linesep
            cells_source = "|"
            for cell in row:
                cells_source = cells_source + cell + "||"
            rows_source = rows_source + cells_source[:-2] + os.linesep
        tables_source = tables_source + rows_source + "|}\n"
    return tables_source

def maintain():
    scraperwiki.sqlite.execute("DROP TABLE table_pages")
    scraperwiki.sqlite.execute("CREATE TABLE table_pages (id TEXT PRIMARY KEY, python_table BLOB, date TEXT)")
#maintain()

page = "Comparison of open source software hosting facilities"
python_table = markup_to_python(get_markup(page))

#print len(base64.b64encode(bz2.compress(buffer(cPickle.dumps(python_table,2))))) #12076
#print len(base64.b64encode(cPickle.dumps(python_table,2)))                       #38404
#print len(cPickle.dumps(python_table,0))                                         #32967
scraperwiki.sqlite.execute("INSERT INTO table_pages values(?,?,?)", (page, cPickle.dumps(python_table,0), str(datetime.date.today())))
#datetime.datetime.strptime(z,"%Y-%m-%d")
scraperwiki.sqlite.commit()


