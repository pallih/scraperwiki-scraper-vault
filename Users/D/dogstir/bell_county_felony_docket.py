try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from itertools import islice, tee, izip

import requests

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    iterable = iter(iterable)
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def iterskip(iterator, test, n):
    """Iterate skipping values matching test, and n following values"""
    iterator = iter(iterator)
    while 1:
        value = next(iterator)
        if test(value):
            for dummy in range(n):
                next(iterator)
        else:
            yield value

def iterchunks(iterator, n):
    """Iterate returning n results at a time"""
    iterator = iter(iterator)
    return izip(*([iterator]*n))

def parse_line(line, fields):
    """Parses a line of fixed width data.
    Fields should be a list of tuples of form:
    (field_start, field_name), field_start being the column number at which the
    field begins.

    """
    data = {}
    field_starts = [field[0] for field in fields]
    # Construct slices ranging from the start of each field to the start of the
    # next field.
    slices = [slice(a, b) for a, b in pairwise(field_starts + [None])]
    for slice_, field in zip(slices, fields):
        field_name = field[1]
        value = line[slice_].strip()
        data[field_name] = value
    return data

def parse_entry(lines, fields):
    """Takes a sequence of fixed width data lines, and extracts the data, mapping
    it to the field names, and returning a dictionary.

    """
    parsed_entry = {}
    for line, line_fields in zip(lines, fields):
        line_data = parse_line(line, line_fields)
        parsed_entry = dict(parsed_entry, **line_data)
    return parsed_entry

def iterparse_lines(lines, fields):
    rows_per_entry = len(fields)
    for line_group in iterchunks(lines, rows_per_entry):
        parsed_entry = parse_entry(line_group, fields)
        yield parsed_entry

def remove_lines_up_to(text, test):
    while True:
        try:
            line, rest = text.split('\n', 1)
        except ValueError:
            return ''

        if test(line):
            return '\n'.join([line, rest])
        else:
            text = rest

def extract_docket_text(page):
    docket = remove_lines_up_to(page, is_heading)
    docket = docket.rsplit('</PRE>')[0] # Yuck..
    return docket

def is_heading(line):
    return 'B E L L   C O U N T Y' in line

def iterparse_fromstring(text, fields):
    return iterparse(StringIO(text), fields)

def iterparse(fh, fields):
    """Iteratively parse a bell county court docket"""
    lines = (line.rstrip('\r\n') for line in fh)

    # skip all heading lines and the following 4 lines.
    data_lines = iterskip(lines, is_heading, 4)
    for result in iterparse_lines(data_lines, fields):
        yield result

if __name__ == 'scraper':
    FIELDS = [
    [(0, 'COURT'),
    (4, 'CAUSE NUMBER'),
    (15, 'SETTING DATE'),
    (20, 'SETTING'),
    (23, 'SETTING TIME'),
    (28, 'MISC'),
    (32, 'DEFENDANT'),
    (59, 'LEVEL'),
    (61, 'OFFENSE'),
    (87, 'ARREST DATE'),
    (92, 'OFFENSE DATE'),
    (97, 'INDICT DATE'),
    (102, 'DEFENSE ATTY'),
    (110, 'PROSECUTOR'),
    (118, 'BOND COMPANY'),
    (121, 'BOND AMOUNT'),
    (128, 'DISPOSITION')],

    []    ]
    
    page = requests.get('http://www.bellcountytx.com/districtcoord/CSTMR/cjdo0001r.htm').content
    
    docket = extract_docket_text(page)

    try:
        from scraperwiki.sqlite import save    
    except:
        def save(a,b,c):
            print b
    for result in iterparse_fromstring(docket, FIELDS):
        save([],result)try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from itertools import islice, tee, izip

import requests

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    iterable = iter(iterable)
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def iterskip(iterator, test, n):
    """Iterate skipping values matching test, and n following values"""
    iterator = iter(iterator)
    while 1:
        value = next(iterator)
        if test(value):
            for dummy in range(n):
                next(iterator)
        else:
            yield value

def iterchunks(iterator, n):
    """Iterate returning n results at a time"""
    iterator = iter(iterator)
    return izip(*([iterator]*n))

def parse_line(line, fields):
    """Parses a line of fixed width data.
    Fields should be a list of tuples of form:
    (field_start, field_name), field_start being the column number at which the
    field begins.

    """
    data = {}
    field_starts = [field[0] for field in fields]
    # Construct slices ranging from the start of each field to the start of the
    # next field.
    slices = [slice(a, b) for a, b in pairwise(field_starts + [None])]
    for slice_, field in zip(slices, fields):
        field_name = field[1]
        value = line[slice_].strip()
        data[field_name] = value
    return data

def parse_entry(lines, fields):
    """Takes a sequence of fixed width data lines, and extracts the data, mapping
    it to the field names, and returning a dictionary.

    """
    parsed_entry = {}
    for line, line_fields in zip(lines, fields):
        line_data = parse_line(line, line_fields)
        parsed_entry = dict(parsed_entry, **line_data)
    return parsed_entry

def iterparse_lines(lines, fields):
    rows_per_entry = len(fields)
    for line_group in iterchunks(lines, rows_per_entry):
        parsed_entry = parse_entry(line_group, fields)
        yield parsed_entry

def remove_lines_up_to(text, test):
    while True:
        try:
            line, rest = text.split('\n', 1)
        except ValueError:
            return ''

        if test(line):
            return '\n'.join([line, rest])
        else:
            text = rest

def extract_docket_text(page):
    docket = remove_lines_up_to(page, is_heading)
    docket = docket.rsplit('</PRE>')[0] # Yuck..
    return docket

def is_heading(line):
    return 'B E L L   C O U N T Y' in line

def iterparse_fromstring(text, fields):
    return iterparse(StringIO(text), fields)

def iterparse(fh, fields):
    """Iteratively parse a bell county court docket"""
    lines = (line.rstrip('\r\n') for line in fh)

    # skip all heading lines and the following 4 lines.
    data_lines = iterskip(lines, is_heading, 4)
    for result in iterparse_lines(data_lines, fields):
        yield result

if __name__ == 'scraper':
    FIELDS = [
    [(0, 'COURT'),
    (4, 'CAUSE NUMBER'),
    (15, 'SETTING DATE'),
    (20, 'SETTING'),
    (23, 'SETTING TIME'),
    (28, 'MISC'),
    (32, 'DEFENDANT'),
    (59, 'LEVEL'),
    (61, 'OFFENSE'),
    (87, 'ARREST DATE'),
    (92, 'OFFENSE DATE'),
    (97, 'INDICT DATE'),
    (102, 'DEFENSE ATTY'),
    (110, 'PROSECUTOR'),
    (118, 'BOND COMPANY'),
    (121, 'BOND AMOUNT'),
    (128, 'DISPOSITION')],

    []    ]
    
    page = requests.get('http://www.bellcountytx.com/districtcoord/CSTMR/cjdo0001r.htm').content
    
    docket = extract_docket_text(page)

    try:
        from scraperwiki.sqlite import save    
    except:
        def save(a,b,c):
            print b
    for result in iterparse_fromstring(docket, FIELDS):
        save([],result)