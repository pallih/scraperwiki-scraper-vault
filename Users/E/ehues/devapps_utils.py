# Utility functions

from cgi import escape

WARDS = ['',
    "Orleans",
    "Innes",
    "Barrhaven",
    "Kanata North",
    "West Carleton-March",
    "Stittsville",
    "Bay",
    "College",
    "Knoxdale-Merivale",
    "Gloucester-Southgate",
    "Beacon Hill-Cyrville",
    "Rideau-Vanier",
    "Rideau-Rockcliffe",
    "Somerset",
    "Kitchissippi",
    "River",
    "Capital",
    "Alta Vista",
    "Cumberland",
    "Osgoode",
    "Rideau-Goulbourn",
    "Gloucester-South Nepean",
    "Kanata South"
]

def application_diff(pair):
    '''Diff a pair of rows from the Applications table. 

    Expect an array as args. The array has two elements, the first is the new item, the second is the old item.

    Return value: dictionary keyed on field name. The values are arrays containing the new value and the old value.
    '''
    book_keeping_fields = {'Last_Scrape' : 0, 'Date_Status' : 0, 'Application_URI' : 0, 'Status_Hash' : 0, 'Current' : 0}
    diff = {}
    for k in pair[0].keys():
        if book_keeping_fields.has_key(k):
            continue

        try:
            if pair[0][k] != pair[1][k]:
                diff[k] = [pair[0][k], pair[1][k]]
        except KeyError:
            continue # We get these when we have columns in pair[0] that don't exist in p[1] due to joins.

    return diff


def stringify_diff(d):
    """Return an unescaped string containing a table that shows a diff returned by application_diff."""
    out = "<table border='1' width='100%'>"
    for k in d.keys():
        out += '''<tr><td rowspan="2" valign="top">%s</td><td>%s</td></tr><tr><td><strike>%s</strike></td></tr>''' % (escape(k), escape(str(d[k][0])), escape(str(d[k][1])))

    out += "</table>"
    return out# Utility functions

from cgi import escape

WARDS = ['',
    "Orleans",
    "Innes",
    "Barrhaven",
    "Kanata North",
    "West Carleton-March",
    "Stittsville",
    "Bay",
    "College",
    "Knoxdale-Merivale",
    "Gloucester-Southgate",
    "Beacon Hill-Cyrville",
    "Rideau-Vanier",
    "Rideau-Rockcliffe",
    "Somerset",
    "Kitchissippi",
    "River",
    "Capital",
    "Alta Vista",
    "Cumberland",
    "Osgoode",
    "Rideau-Goulbourn",
    "Gloucester-South Nepean",
    "Kanata South"
]

def application_diff(pair):
    '''Diff a pair of rows from the Applications table. 

    Expect an array as args. The array has two elements, the first is the new item, the second is the old item.

    Return value: dictionary keyed on field name. The values are arrays containing the new value and the old value.
    '''
    book_keeping_fields = {'Last_Scrape' : 0, 'Date_Status' : 0, 'Application_URI' : 0, 'Status_Hash' : 0, 'Current' : 0}
    diff = {}
    for k in pair[0].keys():
        if book_keeping_fields.has_key(k):
            continue

        try:
            if pair[0][k] != pair[1][k]:
                diff[k] = [pair[0][k], pair[1][k]]
        except KeyError:
            continue # We get these when we have columns in pair[0] that don't exist in p[1] due to joins.

    return diff


def stringify_diff(d):
    """Return an unescaped string containing a table that shows a diff returned by application_diff."""
    out = "<table border='1' width='100%'>"
    for k in d.keys():
        out += '''<tr><td rowspan="2" valign="top">%s</td><td>%s</td></tr><tr><td><strike>%s</strike></td></tr>''' % (escape(k), escape(str(d[k][0])), escape(str(d[k][1])))

    out += "</table>"
    return out