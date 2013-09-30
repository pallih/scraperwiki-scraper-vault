import urllib2
import scraperwiki as sw
from lxml import etree
from unidecode import unidecode
import re
from collections import defaultdict
from cStringIO import StringIO

def parse_pdf(url):
    pdf_data = urllib2.urlopen(url).read()
    assert len(pdf_data) > 0
    
    xml_data = sw.pdftoxml(pdf_data)
    tree = etree.parse(StringIO(xml_data))
    root = tree.getroot()
    print root.xpath('//*text[left<200]')
    #xml = lxml.fromstring(xml_data)

    #p1 = xml.cssselect("page")[0]
    #p1_nodes = [parse_node(node) for node in p1.cssselect("text")]
    
    #low_top = int(text_is(r'2010.+2011\s+Enrollment\s+=', p1_nodes)[0]['top'])
    #up_top = int(text_is(r'SPED', p1_nodes)[0]['top'])
    #low_left = int(text_is(r'All\s+Students', p1_nodes)[0]['left'])
    #up_left = int(text_is(r'MU', p1_nodes)[0]['left'])
    
    # fn
    #bound_fn = table_bound_fn(low_top, up_top, low_left, up_left)

    #bound_nodes = bound_by(bound_fn, p1_nodes)
    #build_table(bound_nodes)


def build_table(table_nodes):
    "Builds a 2d list representation of a table, given a table's nodes."
    column_vals = get_column_vals(table_nodes, ['Female', 'Male', 'AM', 'AS', 'BL', 'HI', 'PI', 'WH', 'MU'])
    row_vals = get_row_vals(table_nodes, ['All Students', 'ESOL', 'FARMS', 'SPED'])
    
    columns = sortby_columns(table_nodes, column_vals)


def sortby_columns(nodes, vals):
    "Returns a list of nodes grouped by column vals."
    column_dict = defaultdict(list)
    
    for node in nodes:
        for val in vals:
            if node['left'] <= val <= (node['left'] + node['width']):
                column_dict[val].append(node)

    return [column_dict[key] for key in column_dict]


def get_column_vals(nodes, keys):
    """Returns a list of column x-coord estimates given a set of keys that exist in nodes.
    Assumes each key is unique in nodes."""
    return [column_line(node) for node in key_nodes(nodes, keys)]


def get_row_vals(nodes, keys):
    """Returns a list of row y-coords ('top' attribute) given a set of keys that
    exists in nodes. Assumes each key is unique in nodes."""
    return [node['top'] for node in key_nodes(nodes, keys)]


def key_nodes(nodes, keys):
    matches = mult_text_is(keys, nodes)
    return [matches[key] for key in matches]


def parse_node(node):
    "Returns a dict representation of a xml node."
    return {'top': float(node.get('top')),
            'left': float(node.get('left')),
            'width': float(node.get('width')),
            'height': float(node.get('height')),
            'text': node.text_content(),
            'node': node}


def bound_by(bound_test, nodes):
    "Returns a list of nodes bound by fn bound_test"
    return [node for node in nodes if bound_test(node['top'], node['left'])]


def column_line(node):
    "Returns an x value representing a vertical line. Accepts a node."
    return node['left'] + (node['width'] / 2)


def get_tl(node):
    "Returns top and left int values for a node."
    return (node['top'], node['left'])


def text_is(regex, nodes):
    """Accepts a regex and a list of lxml nodes and returns a list of nodes, the
    text_content() of which matches the regex."""
    return [node for node in nodes if re.search(regex, unidecode(node['node'].text_content()))]
    

def uniq_text_is(regex, nodes):
    return text_is(regex, nodes)[0]


def mult_text_is(re_list, nodes):
    """Accepts a list of regexs, and returns a dict with a regex as the key and
    matched node as value."""
    matches = {}
    for node in nodes:
        for regex in re_list:
            if re.search(regex, unicode(node['node'].text_content())):
                matches[regex] = node
    return matches


def table_bound_fn(low_top, up_top, low_left, up_left):
    return lambda t, l: (low_top <= t <= up_top and low_left <= l <= up_left)
    

def filter_xml_nodes(nodes, tables):
    for node in nodes:
        for table in tables:
            if table['test'](get_bounds(node)):
                table['nodes'].append(node)


parse_pdf('http://montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/fy2011/schools/02777.pdf')

import urllib2
import scraperwiki as sw
from lxml import etree
from unidecode import unidecode
import re
from collections import defaultdict
from cStringIO import StringIO

def parse_pdf(url):
    pdf_data = urllib2.urlopen(url).read()
    assert len(pdf_data) > 0
    
    xml_data = sw.pdftoxml(pdf_data)
    tree = etree.parse(StringIO(xml_data))
    root = tree.getroot()
    print root.xpath('//*text[left<200]')
    #xml = lxml.fromstring(xml_data)

    #p1 = xml.cssselect("page")[0]
    #p1_nodes = [parse_node(node) for node in p1.cssselect("text")]
    
    #low_top = int(text_is(r'2010.+2011\s+Enrollment\s+=', p1_nodes)[0]['top'])
    #up_top = int(text_is(r'SPED', p1_nodes)[0]['top'])
    #low_left = int(text_is(r'All\s+Students', p1_nodes)[0]['left'])
    #up_left = int(text_is(r'MU', p1_nodes)[0]['left'])
    
    # fn
    #bound_fn = table_bound_fn(low_top, up_top, low_left, up_left)

    #bound_nodes = bound_by(bound_fn, p1_nodes)
    #build_table(bound_nodes)


def build_table(table_nodes):
    "Builds a 2d list representation of a table, given a table's nodes."
    column_vals = get_column_vals(table_nodes, ['Female', 'Male', 'AM', 'AS', 'BL', 'HI', 'PI', 'WH', 'MU'])
    row_vals = get_row_vals(table_nodes, ['All Students', 'ESOL', 'FARMS', 'SPED'])
    
    columns = sortby_columns(table_nodes, column_vals)


def sortby_columns(nodes, vals):
    "Returns a list of nodes grouped by column vals."
    column_dict = defaultdict(list)
    
    for node in nodes:
        for val in vals:
            if node['left'] <= val <= (node['left'] + node['width']):
                column_dict[val].append(node)

    return [column_dict[key] for key in column_dict]


def get_column_vals(nodes, keys):
    """Returns a list of column x-coord estimates given a set of keys that exist in nodes.
    Assumes each key is unique in nodes."""
    return [column_line(node) for node in key_nodes(nodes, keys)]


def get_row_vals(nodes, keys):
    """Returns a list of row y-coords ('top' attribute) given a set of keys that
    exists in nodes. Assumes each key is unique in nodes."""
    return [node['top'] for node in key_nodes(nodes, keys)]


def key_nodes(nodes, keys):
    matches = mult_text_is(keys, nodes)
    return [matches[key] for key in matches]


def parse_node(node):
    "Returns a dict representation of a xml node."
    return {'top': float(node.get('top')),
            'left': float(node.get('left')),
            'width': float(node.get('width')),
            'height': float(node.get('height')),
            'text': node.text_content(),
            'node': node}


def bound_by(bound_test, nodes):
    "Returns a list of nodes bound by fn bound_test"
    return [node for node in nodes if bound_test(node['top'], node['left'])]


def column_line(node):
    "Returns an x value representing a vertical line. Accepts a node."
    return node['left'] + (node['width'] / 2)


def get_tl(node):
    "Returns top and left int values for a node."
    return (node['top'], node['left'])


def text_is(regex, nodes):
    """Accepts a regex and a list of lxml nodes and returns a list of nodes, the
    text_content() of which matches the regex."""
    return [node for node in nodes if re.search(regex, unidecode(node['node'].text_content()))]
    

def uniq_text_is(regex, nodes):
    return text_is(regex, nodes)[0]


def mult_text_is(re_list, nodes):
    """Accepts a list of regexs, and returns a dict with a regex as the key and
    matched node as value."""
    matches = {}
    for node in nodes:
        for regex in re_list:
            if re.search(regex, unicode(node['node'].text_content())):
                matches[regex] = node
    return matches


def table_bound_fn(low_top, up_top, low_left, up_left):
    return lambda t, l: (low_top <= t <= up_top and low_left <= l <= up_left)
    

def filter_xml_nodes(nodes, tables):
    for node in nodes:
        for table in tables:
            if table['test'](get_bounds(node)):
                table['nodes'].append(node)


parse_pdf('http://montgomeryschoolsmd.org/departments/regulatoryaccountability/glance/fy2011/schools/02777.pdf')

